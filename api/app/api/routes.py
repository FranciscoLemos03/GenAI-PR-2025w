from fastapi import APIRouter, Header, HTTPException
from app.models.schemas import GenerateRequest, GenerateResponse

router = APIRouter(prefix="/api")

@router.post("/generate", response_model=GenerateResponse)
def generate(
    data: GenerateRequest,
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Por agora só devolvemos o que recebemos
    return {
        "status": "received",
        "theme": data.theme
    }
