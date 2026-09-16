"""
Backend API tests.

Covers the two cases required by the assignment:
  1. A happy-path /query request that returns a grounded answer + sources.
  2. An invalid /query request (empty question) that returns HTTP 422.

Plus a couple of extra cases (missing field, /health) since they're cheap
and catch real regressions.

These tests use the fake RetrievalService/GenerationService installed in
conftest.py, so they run without needing Ollama or a real vector store.
"""

import pytest
from fastapi.testclient import TestClient

import app.main as main_module


@pytest.fixture
def client():
    # Using TestClient as a context manager triggers FastAPI's lifespan
    # (startup/shutdown) events, which is what populates app.state.retriever
    # and app.state.generator. Without the `with`, those never get set.
    with TestClient(main_module.app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["collection"] == "docs"
    assert data["chunks"] == 42


def test_query_happy_path(client):
    response = client.post(
        "/query",
        json={"question": "What is gradient descent?"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert data["sources"] == ["Lecture 8 Deep Learning.pdf"]
    assert "gradient descent" in data["answer"].lower()


def test_query_invalid_input_empty_question(client):
    response = client.post(
        "/query",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_query_invalid_input_missing_field(client):
    response = client.post(
        "/query",
        json={},
    )

    assert response.status_code == 422
