from pydantic import BaseModel

class GenerateRequest(BaseModel):
    theme: str

class GenerateResponse(BaseModel):
    status: str
    theme: str
