# ai_service.py

import os
import requests
import tempfile
from datetime import datetime
from data_manager import DataManager
from baseline_retriever import BaselineRetriever


dm = DataManager()
retriever = BaselineRetriever()


def upload_pdf_from_firebase(
    file_url: str,
    title: str,
    researcher: str,
    day: str = None
):
    """
    Downloads a PDF from Firebase Storage and indexes it in the vector DB
    """
    if not day:
        day = datetime.now().date().isoformat()

    # 1. Download PDF from Firebase Storage
    response = requests.get(file_url)
    response.raise_for_status()

    # 2. Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        temp_path = tmp.name

    try:
        # 3. Index PDF
        entry = dm.upload_pdf(
            file_path=temp_path,
            title=title,
            day=day,
            researcher=researcher
        )
        return {
            "status": "success",
            "paper_id": entry["id"],
            "title": title
        }
    finally:
        os.remove(temp_path)

def retrieve_from_query(query: str, threshold=0.5):
    """
    Semantic search over indexed PDFs
    """
    results = retriever.search(query, threshold=threshold)

    return {
        "query": query,
        "results": results
    }
