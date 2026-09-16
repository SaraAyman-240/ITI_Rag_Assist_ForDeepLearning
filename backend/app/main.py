from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router as query_router
from app.core.config import FRONTEND_ORIGIN
from app.services.generation import GenerationService
from app.services.retrieval import RetrievalService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load expensive RAG resources once when FastAPI starts.
    """

    print("Starting RAG backend...")

    app.state.retriever = RetrievalService()
    app.state.generator = GenerationService()

    print("RAG backend is ready.")

    yield

    print("RAG backend stopped.")


app = FastAPI(
    title="RAG Study Assistant API",
    description=(
        "FastAPI backend for the "
        "RAG-powered study assistant."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_ORIGIN,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health(request: Request):
    """
    Check whether the API and vector store are running.
    """

    retriever = request.app.state.retriever

    return {
        "status": "ok",
        "collection": retriever.collection.name,
        "chunks": retriever.collection.count(),
    }


app.include_router(query_router)