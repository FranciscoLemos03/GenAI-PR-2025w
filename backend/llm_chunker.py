import os
import fitz
import json
import requests
import time
import re
import uuid
from embedder import Embedder
from dotenv import load_dotenv
from pathlib import Path

# =========================
# CONFIG
# =========================

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMMA_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GEMMA_API_KEY not found in .env")

GEMMA_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemma-3-27b-it:generateContent"
)

PDF_FOLDER = "example_pdfs_to_upload"
OUTPUT_FILE = "llm_database.json"

MAX_CHARS_PER_CALL = 12000
SLEEP_BETWEEN_CALLS = 0.5

embedder = Embedder()

# =========================
# PDF EXTRACTION
# =========================

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def rough_chunk_text(text, max_chars=MAX_CHARS_PER_CALL):
    blocks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        blocks.append(text[start:end])
        start = end
    return blocks


# =========================
# GEMMA
# =========================

def call_gemma(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 2048
        }
    }

    response = requests.post(GEMMA_URL, headers=headers, json=body)
    response.raise_for_status()

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# =========================
# METADATA EXTRACTION
# =========================

META_REGEX_TITLE = re.compile(r"<TITLE>(.*?)</TITLE>", re.DOTALL)
META_REGEX_AUTHORS = re.compile(r"<AUTHORS>(.*?)</AUTHORS>", re.DOTALL)
CHUNK_REGEX = re.compile(r"<CHUNK>(.*?)</CHUNK>", re.DOTALL)


def extract_metadata_and_chunks(text: str, pdf_name: str):
    blocks = rough_chunk_text(text)
    all_chunks = []
    title = None
    researchers = []

    for i, block in enumerate(blocks):
        print(f"🤖 {pdf_name} — block {i+1}/{len(blocks)}")

        prompt = f"""
You are a document analysis system.

From the text below:
1) Extract the paper TITLE (usually first main heading)
2) Extract the AUTHORS (names only, comma separated)
3) Split the text into semantically coherent chunks

Rules:
- Do NOT summarize
- Preserve original text
- 150–300 words per chunk
- Output ONLY in this format:

<TITLE>
title here
</TITLE>

<AUTHORS>
Author One, Author Two, Author Three
</AUTHORS>

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

        raw = call_gemma(prompt)

        if not title:
            t = META_REGEX_TITLE.findall(raw)
            if t:
                title = t[0].strip()

        if not researchers:
            a = META_REGEX_AUTHORS.findall(raw)
            if a:
                researchers = [
                    name.strip()
                    for name in a[0].split(",")
                    if name.strip()
                ]

        chunks = CHUNK_REGEX.findall(raw)
        all_chunks.extend([c.strip() for c in chunks])

        time.sleep(SLEEP_BETWEEN_CALLS)

    return title, researchers, all_chunks


# =========================
# PIPELINE
# =========================

def process_pdf(pdf_path: str):
    pdf_name = os.path.basename(pdf_path)

    print(f"\n📄 Processing: {pdf_name}")

    text = extract_text_from_pdf(pdf_path)

    title, researchers, chunks = extract_metadata_and_chunks(
        text,
        pdf_name
    )

    document = {
        "id": str(uuid.uuid4()),
        "title": title or pdf_name,
        "pdf_name": pdf_name,
        "researchers": researchers,
        "chunks": []
    }

    for i, chunk_text in enumerate(chunks):
        print(f"🧬 Embedding chunk {i+1}/{len(chunks)}")

        embedding = embedder.encode(chunk_text)

        document["chunks"].append({
            "id": i + 1,
            "text": chunk_text,
            "embedding": embedding
        })

    return document


# =========================
# MAIN
# =========================

def main():
    if not os.path.exists(PDF_FOLDER):
        print(f"❌ Folder not found: {PDF_FOLDER}")
        return

    # -----------------------
    #  Load existing base
    # -----------------------
    if os.path.exists(OUTPUT_FILE):
        print(f"📂 Loading existing base: {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            database = json.load(f)
    else:
        print("📄 No existing database found. Create a new one.")
        database = []

    # Create quick set for lookup
    existing_pdfs = {
        doc.get("pdf_name")
        for doc in database
        if "pdf_name" in doc
    }

    # -----------------------
    # Find PDFs
    # -----------------------
    pdfs = [
        f for f in os.listdir(PDF_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    if not pdfs:
        print("⚠️ No PDF found")
        return

    print(f"📚 Found {len(pdfs)} PDFs")
    print(f"🧠 Already processed PDFs: {len(existing_pdfs)}")

    # -----------------------
    # Processar só os novos
    # -----------------------
    for pdf in pdfs:
        if pdf in existing_pdfs:
            print(f"⏭️ Skipping (already exist): {pdf}")
            continue

        doc = process_pdf(os.path.join(PDF_FOLDER, pdf))
        database.append(doc)

        # Guarda incrementalmente (segurança contra crash)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(database, f, ensure_ascii=False, indent=2)

    print(f"\n🔥 Updated database: {OUTPUT_FILE}")
    print(f"📄 Total documents: {len(database)}")

if __name__ == "__main__":
    main()