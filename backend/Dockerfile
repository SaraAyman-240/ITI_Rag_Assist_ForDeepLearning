FROM python:3.10-slim

WORKDIR /app

# build-essential is needed for a couple of chromadb/sentence-transformers
# transitive dependencies that compile C extensions on install.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# The persisted vector store already lives in ./data/vector_store, so the
# app loads it at startup instead of rebuilding it. The container still
# needs network access to an Ollama instance (e.g. host.docker.internal,
# or a linked service) reachable at the host/port your client expects.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
