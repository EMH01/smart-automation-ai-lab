from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_invalid_question():
    assert client.post("/ask", json={"question": "a"}).status_code == 422

def test_missing_cloud_config(monkeypatch):
    for item in ("AZURE_SEARCH_ENDPOINT", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"):
        monkeypatch.delenv(item, raising=False)
    r = client.post("/ask", json={"question": "How do I request leave?"})
    assert r.status_code == 503
