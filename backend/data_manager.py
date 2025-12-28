# data_manager.py
import os
import uuid
import fitz
import json
import tempfile
import requests
from embedder import Embedder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this .py is located
METADATA_FILE = os.path.join(BASE_DIR, "data", "metadata.json")
PDF_FOLDER = os.path.join(BASE_DIR, "data", "pdfs")
EXAMPLE_FOLDER = os.path.join(BASE_DIR, "example_pdfs_to_upload")

class DataManager:
    """
    Handles everything related to:
    - downloading or receiving PDFs
    - saving them to the database
    - extracting text
    - chunking, embedding & storing metadata
    """

    def __init__(self, metadata_file=METADATA_FILE, pdf_folder=PDF_FOLDER):
        self.embedder = Embedder()
        self.metadata_file = metadata_file
        self.pdf_folder = pdf_folder
        self.metadata = self.load_metadata()

    # ------------------------------
    # METADATA I/O
    # ------------------------------
    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_metadata(self):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4, ensure_ascii=False)

    # ------------------------------
    # INTERNAL UTILITIES
    # ------------------------------
    def _save_pdf_to_db(self, file_path):
        """Assigns a DB filename and copies the PDF inside /data/pdfs."""
        pdf_name = f"{uuid.uuid4()}.pdf"
        out_path = os.path.join(self.pdf_folder, pdf_name)
        with open(file_path, "rb") as src, open(out_path, "wb") as dst:
            dst.write(src.read())
        return pdf_name

    def _create_metadata_entry(self, title, pdf_name, researcher, abstract=""):
        entry = {
            "id": str(uuid.uuid4()),
            "title": title,
            "pdf_name": pdf_name,
            "researcher": researcher,
            "abstract": abstract,
            "chunks": []  # filled after processing
        }
        self.metadata.append(entry)
        self.save_metadata()
        return entry
    

    # ------------------------------
    # PUBLIC API: MAIN UPLOAD METHODS
    # ------------------------------

    def upload_pdf(self, file_path, title, researcher, abstract=""):
        """UPLOAD from a local file path and index it immediately."""
        self.metadata = self.load_metadata()
        pdf_name = self._save_pdf_to_db(file_path)
        entry = self._create_metadata_entry(title, pdf_name, researcher, abstract)
        self.process_pdf(entry)
        print(f"Uploaded & indexed: {title}")
        return entry

    def upload_pdf_from_url(self, url, title, researcher, abstract=""):
        """DOWNLOAD FROM URL → add to DB → chunk & embed."""
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp.write(requests.get(url).content)
        temp.close()
        return self.upload_pdf(temp.name, title, researcher, abstract)

    def save_example_pdf(self, url):
        """Download a PDF but do NOT process or embed it. (Training examples)"""
        filename = url.split("/")[-1]
        out_path = os.path.join(EXAMPLE_FOLDER, filename)

        if not os.path.exists(out_path):
            with open(out_path, "wb") as f:
                f.write(requests.get(url).content)
            print("Saved example:", out_path)
        else:
            print("Example already exists:", out_path)

        return out_path

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
        chunks = self.chunk_text(text)

        entry["chunks"] = [
            {
                "id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": self.embedder.encode(chunk)
            }
            for chunk in chunks
        ]

        self.save_metadata()
        print(f"Indexed {len(chunks)} chunks for: {entry['title']}")
        return entry
