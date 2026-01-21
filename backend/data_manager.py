# data_manager.py
import os
import re
import uuid
import fitz
import json
import time
import requests
from embedder import Embedder
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this .py is located
DATABASE_FILE = os.path.join(BASE_DIR, "data", "database.json")
PDF_FOLDER = os.path.join(BASE_DIR, "data", "pdfs")
EXAMPLE_FOLDER = os.path.join(BASE_DIR, "example_pdfs_to_upload")

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

GEMMA_API_KEY = os.environ.get("GEMMA_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMMA_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

class DataManager:
    """
    Handles everything related to:
    - downloading or receiving PDFs
    - saving them to the database
    - extracting text
    - chunking, embedding & storing database
    """

    def __init__(self, database_file=DATABASE_FILE, pdf_folder=PDF_FOLDER):
        self.embedder = Embedder()
        self.database_file = database_file
        self.pdf_folder = pdf_folder
        self.database = self.load_database()

    # ------------------------------
    # DATABASE I/O
    # ------------------------------
    def load_database(self):
        if os.path.exists(self.database_file):
            with open(self.database_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_database(self):
        with open(self.database_file, "w", encoding="utf-8") as f:
            json.dump(self.database, f, indent=4, ensure_ascii=False)

    # ------------------------------
    # INTERNAL UTILITIES
    # ------------------------------
    def _save_pdf_to_db(self, file_path, title, day, researcher):
        """Assigns a DB filename and copies the PDF inside /data/pdfs."""
        pdf_name = f"{day}_{researcher.replace(' ', '-')}_{title.replace(' ', '-')}.pdf"
        out_path = os.path.join(self.pdf_folder, pdf_name)
        with open(file_path, "rb") as src, open(out_path, "wb") as dst:
            dst.write(src.read())
        return pdf_name

    def _create_database_entry(self, title, pdf_name, day, researcher):
        if hasattr(day, "isoformat"):
            day_str = day.isoformat()
        else:
            day_str = str(day)  # ya es string tipo "2025-01-07"

        entry = {
            "id": str(uuid.uuid4()),
            "title": title,
            "pdf_name": pdf_name,
            "researcher": researcher,
            "Upload date": day_str,
            "chunks": []  # filled after processing
        }
        self.database.append(entry)
        self.save_database()
        return entry

    # ------------------------------
    # LLM: METADATA EXTRACTION
    # ------------------------------
    def extract_llm_metadata(self, doc_text: str) -> dict:
        """
        Calls Gemini Flash to get structured JSON metadata (Title, Authors, Summary, etc.)
        """
        print("  - Extracting metadata with Gemini...")
        
        # Use first 12k chars to avoid context limits, usually enough for Intro/Header
        snippet = doc_text[:12000]

        prompt = f"""
        You are extracting bibliographic and topical metadata from a PDF text dump.
        Return ONLY valid JSON (no markdown formatting).

        Schema:
        {{
            "authors": [string],
            "year": int|null,
            "keywords": [string],
            "topics": [string],
            "one_sentence_summary": string|null
        }}

        Rules:
        - If unsure, use null or empty lists
        - Do not hallucinate author names
        - Base everything strictly on the provided text

        TEXT:
        {snippet}
        """.strip()

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMMA_API_KEY
        }
        body = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(GEMINI_URL, headers=headers, json=body)
            response.raise_for_status()
            
            data = response.json()
            raw = data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Clean Markdown wrappers if present
            raw = raw.strip().replace("```json", "").replace("```", "").strip()
            
            return json.loads(raw)

        except Exception as e:
            print(f"Metadata extraction failed: {e}")
            # Return empty structure on failure so pipeline doesn't crash
            return {"authors": [], "year": None, 
                "keywords": [], "topics": [], "one_sentence_summary": None}
    
    
    # ------------------------------
    # HELPERS (LLM AND METADATA STRING BUILDER)
    # ------------------------------
    def _rough_chunk_text(self, text, max_chars=12000):
        """
        Splits text into large blocks to fit API context window.
        """
        return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]

    def _call_gemma(self, prompt):
        """
        Sends prompt to Google Gemma API.
        """
        if not GEMMA_API_KEY:
            raise ValueError("GEMMA_API_KEY not found")

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMMA_API_KEY
        }
        body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2048}
        }
        
        try:
            response = requests.post(GEMMA_URL, headers=headers, json=body)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Error calling Gemma: {e}")
            return ""

    def _build_metadata_string(self, llm_meta):
        """
        Formats the metadata dictionary into a structured string for embedding.
        """
        if not llm_meta:
            return ""
            
        parts = []

        if llm_meta.get("year") and isinstance(llm_meta["year"], list):
            parts.append("year: " + ", ".join(llm_meta["year"]))

        if llm_meta.get("author") and isinstance(llm_meta["author"], list):
            parts.append("Autor: " + ", ".join(llm_meta["author"]))
            
        if llm_meta.get("topics") and isinstance(llm_meta["topics"], list):
            parts.append("Topics: " + ", ".join(llm_meta["topics"]))
            
        if llm_meta.get("keywords") and isinstance(llm_meta["keywords"], list):
            parts.append("Keywords: " + ", ".join(llm_meta["keywords"]))
            
        if llm_meta.get("one_sentence_summary"):
            parts.append("Summary: " + llm_meta["one_sentence_summary"])
            
        return "[METADATA]\n" + "\n".join(parts)


    # ------------------------------
    # PROCESSING (LLM CHUNKING + EMBEDDING)
    # ------------------------------
    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text


    def chunk_text(self, text):
        """
        Uses Gemma to split text into semantic chunks.
        Returns a list of strings.
        """
        CHUNK_REGEX = re.compile(r"<CHUNK>(.*?)</CHUNK>", re.DOTALL)
        
        # 1. Split into large blocks for the API
        blocks = self._rough_chunk_text(text)
        all_semantic_chunks = []

        print(f"Starting LLM Chunking ({len(blocks)} API calls required)...")

        for i, block in enumerate(blocks):
            print(f"  - Processing block {i+1}/{len(blocks)}...")
            
            prompt = f"""
                You are a document analysis system.

                From the text below:
                1) Split the text into semantically coherent chunks
                2) Preserve original text exactly
                3) 150-300 words per chunk
                4) Output ONLY in this format:

                <CHUNK>
                chunk text here
                </CHUNK>

                <CHUNK>
                chunk text here
                </CHUNK>

                TEXT:
                \"\"\"
                {block}
                \"\"\"
                """
            # 2. Call API
            raw_output = self._call_gemma(prompt)
            
            # 3. Parse XML Tags
            found_chunks = CHUNK_REGEX.findall(raw_output)
            clean_chunks = [c.strip() for c in found_chunks if c.strip()]
            
            all_semantic_chunks.extend(clean_chunks)
            
            # Rate limiting
            time.sleep(0.5)

        return all_semantic_chunks


    # ------------------------------
    # MAIN UPLOAD METHODS
    # ------------------------------

    def upload_pdf(self, file_path, title, day, researcher):
        """
        UPLOAD from a local file path and index it immediately.
        """
        self.database = self.load_database()
        pdf_name = self._save_pdf_to_db(file_path, title, day, researcher)
        entry = self._create_database_entry(title, pdf_name, day, researcher)
        self.process_pdf(entry)
        print(f"Successfully uploaded & indexed: {title}")
        return entry


    def process_pdf(self, entry):
        pdf_path = os.path.join(self.pdf_folder, entry["pdf_name"])
        if not os.path.exists(pdf_path):
            print("PDF missing:", pdf_path)
            return

        # 1. Extract raw text
        text = self.extract_text(pdf_path)

        # 2. Extract metadata
        metadata = self.extract_llm_metadata(text)
        entry["metadata"] = metadata

        # 3. Embed metadata and store
        print("  - Embedding metadata...")
        meta_str = self._build_metadata_string(metadata)
        entry["metadata"]["string_representation"] = meta_str
        if meta_str:
            entry["metadata"]["embedding"] = self.embedder.encode(meta_str)
        else:
            entry["metadata"]["embedding"] = []

        # 3. LLM chunking
        chunks = self.chunk_text(text)
        if not chunks:
            print("Warning: No chunks returned from LLM. Using raw text fallback.")
            chunks = [text]

        # 4. Embed chunks and store
        entry["chunks"] = []
        for chunk_text in chunks:
            entry["chunks"].append({
                "id": str(uuid.uuid4()),
                "text": chunk_text,
                "embedding": self.embedder.encode(chunk_text)
            })

        self.save_database()
        print(f"Indexed {len(chunks)} chunks for: {entry['title']}")
        return entry


