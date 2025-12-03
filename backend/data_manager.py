import os
import uuid
import fitz
import json
from sentence_transformers import SentenceTransformer

PDF_FOLDER = "data/pdfs"
METADATA_FILE = "data/metadata.json"
os.makedirs(PDF_FOLDER, exist_ok=True)

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")


class DataManager:
    def __init__(self, metadata_file=METADATA_FILE, pdf_folder=PDF_FOLDER):
        self.metadata_file = metadata_file
        self.pdf_folder = pdf_folder
        self.metadata = self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_metadata(self):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4, ensure_ascii=False)

    def upload_pdf(self, file_path, title, researcher):
        # Copy PDF to data/pdfs
        pdf_name = f"{uuid.uuid4()}.pdf"
        out_path = os.path.join(self.pdf_folder, pdf_name)
        with open(file_path, "rb") as src, open(out_path, "wb") as dst:
            dst.write(src.read())

        # Create metadata entry
        entry = {
            "id": str(uuid.uuid4()),
            "title": title,
            "pdf_name": pdf_name,
            "researcher": researcher
        }
        self.metadata.append(entry)
        self.save_metadata()
        print("PDF uploaded and metadata saved!")
        return entry

    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text

    def chunk_text(self, text, max_chars=1000):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + max_chars, len(text))
            chunks.append(text[start:end])
            start = end
        return chunks

    def generate_embedding(self, text):
        return embedding_model.encode(text).tolist()

    def process_pdf(self, entry):
        pdf_path = os.path.join(self.pdf_folder, entry["pdf_name"])
        if not os.path.exists(pdf_path):
            print("PDF not found:", pdf_path)
            return

        full_text = self.extract_text(pdf_path)
        text_chunks = self.chunk_text(full_text)

        chunks_data = []
        for chunk in text_chunks:
            emb = self.generate_embedding(chunk)
            chunks_data.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": emb
            })
        entry["chunks"] = chunks_data
        self.save_metadata()
        print(f"Processed {len(chunks_data)} chunks for:", entry["title"])
