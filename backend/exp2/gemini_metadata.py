import os, json
import google.generativeai as genai

#EVERYONE NEEDS THEIR API KEY
#environment variable
#Windows powershell => setx GEMINI_API_KEY "YOUR_API_KEY"
#Linux/MacOs => export GEMINI_API_KEY="YOUR_API_KEY"

MODEL = "gemini-2.0-flash"  # buen default para extracción rápida

def extract_llm_metadata(doc_text):
    """
    Returns metadata in JSON from the text of the document
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY env var")

    client = genai.Client(api_key=api_key)

    # recorta para no pasarle el documento entero (suficiente con inicio/abstract)
    snippet = doc_text[:12000]

    prompt = f"""
You are extracting bibliographic and topical metadata from a PDF text dump.
Return ONLY valid JSON (no markdown).

Schema:
{{
  "title": string|null,
  "authors": [string],
  "year": int|null,
  "keywords": [string],   // 8-15 items
  "topics": [string],     // 2-5 short tags
  "one_sentence_summary": string|null
}}

Rules:
- If you are unsure, use null or empty lists.
- Keep keywords/topics concise (1-4 words).
- Do not hallucinate specific author names if not present.
- Base everything only on the provided text.

TEXT:
{snippet}
""".strip()

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = (resp.text or "").strip()
    return json.loads(text)
