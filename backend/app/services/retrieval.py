import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import (
    VECTOR_STORE_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)


class RetrievalService:
    def __init__(self):
        print("Loading embedding model...")

        self.embedder = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Opening persisted ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(VECTOR_STORE_PATH)
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

        print(
            f"Loaded collection '{COLLECTION_NAME}' "
            f"with {self.collection.count()} chunks."
        )

    def retrieve(self, question: str, k: int = 3):
        """
        Convert the user's question into an embedding,
        search ChromaDB, and return the Top-K chunks.
        """

        query_embedding = self.embedder.encode(
            [question]
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k,
        )

        return results