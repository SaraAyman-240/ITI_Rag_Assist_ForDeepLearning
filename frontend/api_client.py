import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# Load frontend/.env
FRONTEND_DIR = Path(__file__).resolve().parent
load_dotenv(FRONTEND_DIR / ".env")


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


def ask_backend(question: str) -> dict:
    """
    Send the user's question to the FastAPI backend
    and return the RAG response.
    """

    response = requests.post(
        f"{API_BASE_URL}/query",
        json={
            "question": question
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()