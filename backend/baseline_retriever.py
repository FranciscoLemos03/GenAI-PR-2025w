import os
import json
import numpy as np
from embedder import Embedder

METADATA_FILE = "data/metadata.json"

class BaselineRetriever:
    def __init__(self, metadata_file=METADATA_FILE):
        self.embedder = Embedder()
        self.metadata_file = metadata_file
        self.metadata = self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def cosine_similarity(self, v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def search(self, query, threshold=0.70):
        """Returns papers ranked by similarity. threshold ~ 0.65-0.80 recommended"""
        query_emb = self.embedder.encode(query)
        results = []

        for entry in self.metadata:
            if "chunks" not in entry:
                continue  # not processed yet
            best_score = 0
            best_chunk = None

            for chunk in entry["chunks"]:
                score = self.cosine_similarity(query_emb, chunk["embedding"])
                if score > best_score:
                    best_score = score
                    best_chunk = chunk

            if best_score >= threshold:
                results.append({
                    "paper_id": entry["id"],
                    "title": entry["title"],
                    "researcher": entry["researcher"],
                    "score": round(best_score, 3),
                    "sample_text": best_chunk["text"][:300] if best_chunk else ""
                })

        # Sort best match → worst
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
