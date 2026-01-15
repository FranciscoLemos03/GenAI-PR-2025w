# data_manager.py
import os
import uuid
import fitz
import json
import tempfile
import requests
from embedder import Embedder

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

    def __init__(self, database_file=DATABASE_FILE, pdf_folder=PDF_FOLDER):
        self.embedder = Embedder()
        self.database_file = database_file
        self.pdf_folder = pdf_folder
        self.database = self.load_database()
        self.tokenizer = self.embedder.model.tokenizer

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
    def _save_pdf_to_db(self, file_path, file_name=None):
        """Assigns a DB filename and copies the PDF inside /data/pdfs."""
        pdf_name = f"{file_name}.pdf"
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

    def upload_pdf(self, file_path, title, researcher, file_name):
        """UPLOAD from a local file path and index it immediately."""
        self.database = self.load_database()
        pdf_name = self._save_pdf_to_db(file_path, file_name)
        entry = self._create_database_entry(title, pdf_name, researcher)
        self.process_pdf(entry)
        print(f"Uploaded & indexed: {title}")
        return entry


    # ------------------------------
    # PROCESSING (CHUNK + EMBEDDING)
    # ------------------------------
    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text

    def chunk_text(self, text, chunk_size=400, chunk_overlap=50):
        # 1. Convert text to token IDs (integers)
        # We use add_special_tokens=False so we don't get [CLS]/[SEP] inside every chunk
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        # 2. Iterate through tokens with a sliding window
        # The step size is (chunk_size - chunk_overlap)
        step = chunk_size - chunk_overlap
        for i in range(0, len(tokens), step):
            # Extract the window of tokens
            chunk_ids = tokens[i : i + chunk_size]
            # 3. Decode back to text
            chunk_text = self.tokenizer.decode(chunk_ids, skip_special_tokens=True)
            chunks.append(chunk_text)
        return chunks

    def process_pdf(self, entry):
        pdf_path = os.path.join(self.pdf_folder, entry["pdf_name"])
        if not os.path.exists(pdf_path):
            print("PDF missing:", pdf_path)
            return

        text = self.extract_text(pdf_path)
        chunks = self.chunk_text(text)

        entry["chunks"] = [
            {
                "id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": self.embedder.encode(chunk)
            }
            for chunk in chunks
        ]

        self.save_database()
        print(f"Indexed {len(chunks)} chunks for: {entry['title']}")
        return entry
