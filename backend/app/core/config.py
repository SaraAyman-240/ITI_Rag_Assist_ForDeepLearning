import json
import os
from pathlib import Path

from dotenv import load_dotenv


# Path to the backend folder
BACKEND_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from backend/.env
load_dotenv(BACKEND_DIR / ".env")


# Vector store folder
VECTOR_STORE_PATH = BACKEND_DIR / "data" / "vector_store"

# Person 1 exported this config with the Chroma database
VECTOR_CONFIG_PATH = VECTOR_STORE_PATH / "config.json"


# Make sure the config exists
if not VECTOR_CONFIG_PATH.exists():
    raise FileNotFoundError(
        f"Vector store config was not found at: {VECTOR_CONFIG_PATH}"
    )


# Read Person 1's RAG settings
with open(VECTOR_CONFIG_PATH, "r", encoding="utf-8") as file:
    vector_config = json.load(file)


CHUNK_SIZE = vector_config["chunk_size"]
CHUNK_OVERLAP = vector_config["chunk_overlap"]
EMBEDDING_MODEL = vector_config["embedding_model"]
OLLAMA_MODEL = vector_config["ollama_model"]
COLLECTION_NAME = vector_config["collection_name"]


# Backend-specific settings
TOP_K = int(os.getenv("TOP_K", "3"))

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:8501",
)