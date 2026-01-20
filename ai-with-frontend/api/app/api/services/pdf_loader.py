import requests
import tempfile
import os


def download_pdf_from_url(url: str) -> str:
    """
    Downloads a PDF and returns a local temp file path
    """
    response = requests.get(url)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        return tmp.name
