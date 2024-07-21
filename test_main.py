import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_query_endpoint():
    response = client.post("/query/", json={"text": "What is the weather today?"})
    assert response.status_code == 200
    assert "response" in response.json()
