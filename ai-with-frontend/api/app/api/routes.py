import os
from fastapi import APIRouter, HTTPException
from datetime import date

from genai.data_manager import DataManager
from genai.baseline_retriever import BaselineRetriever

from ..models.schemas import PDFUploadRequest, SearchRequest, SearchResponse
from .services.pdf_loader import download_pdf_from_url
from .services.room_db import get_room_db_path

router = APIRouter(prefix="/api", tags=["genai"])


# -----------------------------
# PDF UPLOAD ENDPOINT
# -----------------------------

@router.post("/upload_pdf")
def upload_pdf(req: PDFUploadRequest):
    """
    Receives a Firebase Storage URL and indexes the PDF
    into a room-specific vector database
    """

    try:
        # 1. Resolve room-specific DB path
        room_db_path = get_room_db_path(req.roomId)

        # 2. Create DataManager for this room
        dm = DataManager(database_file=room_db_path)

        # 3. Download PDF from Firebase Storage
        temp_path = download_pdf_from_url(str(req.fileURL))

        try:
            # 4. Run full GenAI pipeline
            entry = dm.upload_pdf(
                file_path=temp_path,
                title=req.title,
                day=date.today().isoformat(),
                researcher=req.researcher
            )
        finally:
            os.remove(temp_path)

        return {
            "status": "success",
            "roomId": req.roomId,
            "paper_id": entry["id"],
            "title": entry["title"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# SEARCH ENDPOINT
# -----------------------------

@router.post("/search/{room_id}", response_model=SearchResponse)
def search(room_id: str, req: SearchRequest):
    """
    Runs semantic retrieval over a room-specific vector database
    """

    try:
        room_db_path = get_room_db_path(room_id)
        retriever = BaselineRetriever(database_file=room_db_path)

        results = retriever.search(
            query=req.query,
            threshold=req.threshold
        )

        return {
            "query": req.query,
            "roomId": room_id,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# HEALTH CHECK
# -----------------------------

@router.get("/health")
def health():
    return {"status": "ok"}