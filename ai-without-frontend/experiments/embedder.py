# embedder.py
import numpy as np
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def encode(self, text: str):
        """Generate L2-normalized embeddings for consistency."""
        emb = self.model.encode(text)
        norm = np.linalg.norm(emb)
        emb = emb / (norm + 1e-8)  # normalize
        return emb.tolist()
