# data_manager.py
import os
import uuid
import fitz  #pip install pymupdf
import json
import tempfile
import requests

from embedder import Embedder
from gemini_metadata import extract_llm_metadata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this .py is located
DATABASE_FILE = os.path.join(BASE_DIR, "data", "database.json")
PDF_FOLDER = os.path.join(BASE_DIR, "data", "pdfs")
EXAMPLE_FOLDER = os.path.join(BASE_DIR, "example_pdfs_to_upload")



class DataManager:
    """
    Handles everything related to:
    - downloading or receiving PDFs
    - saving them to the database
    - extracting text
    - chunking, embedding & storing database
    """

    def __init__(self, database_file=DATABASE_FILE, pdf_folder=PDF_FOLDER, metadata_mode = "concat"):
        self.embedder = Embedder()
        self.database_file = database_file
        self.pdf_folder = pdf_folder
        self.database = self.load_database()
        self.metadata_mode = metadata_mode #"concat" or "dual"

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
    def _save_pdf_to_db(self, file_path, arxiv_id=None):
        """Assigns a DB filename and copies the PDF inside /data/pdfs."""
        pdf_name = f"{arxiv_id}.pdf" if arxiv_id else f"{uuid.uuid4()}.pdf"
        out_path = os.path.join(self.pdf_folder, pdf_name)
        with open(file_path, "rb") as src, open(out_path, "wb") as dst:
            dst.write(src.read())
        return pdf_name

    def _create_database_entry(self, title, pdf_name, researcher):
        entry = {
            "id": str(uuid.uuid4()),
            "title": title,
            "pdf_name": pdf_name,
            "researcher": researcher,
            "chunks": []  # filled after processing
        }
        self.database.append(entry)
        self.save_database()
        return entry
    

    # ------------------------------
    # MAIN UPLOAD METHODS
    # ------------------------------

    def upload_pdf(self, file_path, title, researcher, arxiv_id):
        """UPLOAD from a local file path and index it immediately."""
        self.database = self.load_database()
        pdf_name = self._save_pdf_to_db(file_path, arxiv_id)
        entry = self._create_database_entry(title, pdf_name, researcher)
        self.process_pdf(entry)
        print(f"Uploaded & indexed: {title}")
        return entry
    # ------------------------------
    # METADATA
    # ------------------------------
    def build_metadata_string(self, entry): #entry is dict
        m = entry.get("llm_metadata") or {}
        parts = []
        if m.get("title"):
            parts.append(f"Title: {m['title']}")
        if m.get("authors"):
            parts.append("Authors: " + ", ".join(m["authors"][:10]))
        if m.get("year"):
            parts.append(f"Year: {m['year']}")
        if m.get("topics"):
            parts.append("Topics: " + ", ".join(m["topics"]))
        if m.get("keywords"):
            parts.append("Keywords: " + ", ".join(m["keywords"]))
        if m.get("one_sentence_summary"):
            parts.append("Summary: " + m["one_sentence_summary"])

        if not parts:
            return ""

        return "[METADATA]\n" + "\n".join(parts)


    def ensure_llm_metadata(self, entry, doc_text):
        """
        Adds entry['llm_metadata'] if missing. Calls Gemini once per document.
        """
        if entry.get("llm_metadata") is not None:
            return  # already present (even if empty dict)

        try:
            entry["llm_metadata"] = extract_llm_metadata(doc_text)
            self.save_database()  # persist early to avoid repeated calls
        except Exception as e:
            print("Gemini metadata extraction failed:", e)
            entry["llm_metadata"] = {}
            self.save_database()      

    # ------------------------------
    # PROCESSING (CHUNK + EMBEDDING)
    # ------------------------------
    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text

    def chunk_text(self, text, max_chars=1000):
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    def process_pdf(self, entry):
        pdf_path = os.path.join(self.pdf_folder, entry["pdf_name"])
        if not os.path.exists(pdf_path):
            print("PDF missing:", pdf_path)
            return

        text = self.extract_text(pdf_path)

        #metadata doc-level
        self.ensure_llm_metadata(entry, text)
        metadata_str = self.build_metadata_string(entry)
        
        chunks = self.chunk_text(text)

        for chunk in chunks:
            if self.metadata_mode == "concat":
                text_to_embed = chunk + "\n\n" + metadata_str if metadata_str else chunk
                embedding = self.embedder.encode(text_to_embed)

            entry["chunks"].append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": embedding
            })

        self.save_database()
        print(f"Indexed {len(chunks)} chunks for: {entry['title']}")
        return entry
