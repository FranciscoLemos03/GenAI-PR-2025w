import os
import json
import numpy as np
from embedder import Embedder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "data", "database.json")
    


class BaselineRetriever:
    def __init__(self, database_file=DATABASE_FILE):
        self.embedder = Embedder()
        self.database_file = database_file
        self.database = self.load_database()

    def load_database(self):
        if os.path.exists(self.database_file):
            with open(self.database_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def cosine_similarity(self, v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def search(self, query, threshold=0.45, alpha=0.5):
        """
        Returns papers ranked by similarity.
        """    
        self.database = self.load_database()

        if len(self.database) == 0:
            print("Database is empty: no entries to search.\n")

        query_emb = self.embedder.encode(query)
        results = []

        for entry in self.database:
            if "chunks" not in entry:
                continue
            best_score = 0
            best_chunk = None
            metadata = entry["metadata"]

            for chunk in entry["chunks"]:
                # APPLY DUAL EMBEDDINGS
                score_text = self.cosine_similarity(query_emb, chunk["embedding"])
                score_meta = self.cosine_similarity(query_emb, metadata["embedding"])
                score = alpha * score_text + (1 - alpha) * score_meta
                if score > best_score:
                    best_score = score
                    best_chunk = chunk
            
            if best_score >= threshold:
                results.append({
                    "paper_id": entry["id"],
                    "title": entry["title"],
                    "researcher": entry["researcher"],
                    "pdf_name": entry.get("pdf_name", ""),
                    "score": round(best_score, 3),
                    "sample_text": best_chunk["text"][:300] if best_chunk else ""
                })
        # Sort best match --> worst
        results.sort(key=lambda x: x["score"], reverse=True)
        return results