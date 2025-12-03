import os
import json
import requests

# EVERYONE SHOULD HAVE THEIR OWN KEY FOR THE GEMINI API
# FROM https://aistudio.google.com/app/api-keys


class Summarizer:
    def __init__(self, metadata_path="data/metadata.json", api_key=None):
        self.metadata_path = metadata_path
        self.api_key = api_key or "KEY"  # CHANGE PRIVATE KEY HERE
        self.metadata = self._load_metadata()


    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            print("metadata.json not found.")
            return []

        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)


    def _gemini_completion(self, prompt):
        """Generate text using Gemini API (v1beta)."""
        url = ("https://generativelanguage.googleapis.com/v1beta/"
               "models/gemini-2.5-flash:generateContent")
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key}
        payload = { "contents": [{"parts": [{"text": prompt}] }] }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]


    def _combine_chunks(self, chunks, limit=100000):
        """Combine text chunks and truncate safely."""
        combined = "\n\n".join(chunks)
        if len(combined) > limit:
            combined = combined[:limit] + "\n\n...[TRUNCATED]..."
        return combined


    def _summarize_filtered(self, filter_fn, title="SUMMARY"):
        """Generic function to summarize papers filtered by a given function."""
        chunks = []
        for paper in filter(filter_fn, self.metadata):
            chunks.append(f"\n=== PAPER: {paper['title']} ===\n")
            chunks.extend([c["text"] for c in paper["chunks"]])

        if not chunks:
            print(f"No chunks found for {title}. Process PDFs first.")
            return None

        combined_text = self._combine_chunks(chunks)

        prompt = ("You are a scientific summarization assistant.\n"
                  "Summarize the following academic papers clearly and concisely:\n\n"
                  f"{combined_text}")

        summary = self._gemini_completion(prompt)

        print(f"\n===== SUMMARY OF {title} =====\n")
        print(summary)
        print(f"\n{'=' * (20 + len(title))}\n")

        return summary
   
   
    # PUBLIC METHODS
    def summarize_all(self):
        """Summarize ALL papers in metadata.json."""
        self.metadata = self._load_metadata() 

        def all_papers_filter(paper):
            return "chunks" in paper

        return self._summarize_filtered(all_papers_filter, title="COMPLETE SUMMARY")


    def summarize_by_researcher(self, researcher_name):
        """Summarize only papers uploaded/consulted by a specific researcher."""
        self.metadata = self._load_metadata() 

        def researcher_filter(paper):
            return paper.get("researcher") == researcher_name and "chunks" in paper

        return self._summarize_filtered(researcher_filter, title=f"SUMMARY OF DATA UPLOADED BY {researcher_name}")

