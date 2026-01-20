
from pydantic import BaseModel, HttpUrl
from typing import List


class PDFUploadRequest(BaseModel):
    roomId: str
    promptId: str
    title: str
    researcher: str
    fileURL: HttpUrl


class SearchRequest(BaseModel):
    query: str
    threshold: float = 0.5


class SearchResult(BaseModel):
    paper_id: str
    title: str
    researcher: str
    pdf_name: str
    score: float
    sample_text: str


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]