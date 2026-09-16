from fastapi import APIRouter, Request

from app.core.config import TOP_K
from app.schemas.query import (
    QueryRequest,
    QueryResponse,
)


router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query_documents(
    payload: QueryRequest,
    request: Request,
):
    """
    Complete RAG request:

    question
        -> retrieval
        -> prompt
        -> Ollama
        -> answer + sources
    """

    retriever = request.app.state.retriever
    generator = request.app.state.generator

    results = retriever.retrieve(
        question=payload.question,
        k=TOP_K,
    )

    answer = generator.generate(
        question=payload.question,
        results=results,
    )

    sources = []

    for metadata in results["metadatas"][0]:
        source = metadata.get(
            "source",
            "Unknown source",
        )

        if source not in sources:
            sources.append(source)

    return QueryResponse(
        answer=answer,
        sources=sources,
    )