from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="The question the user wants to ask."
    )


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]