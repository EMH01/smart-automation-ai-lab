from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_question():
    assert client.post("/ask", json={"question": "a"}).status_code == 422


def test_missing_cloud_config(monkeypatch):
    for name in ("AZURE_SEARCH_ENDPOINT", "AZURE_FOUNDRY_ENDPOINT", "AZURE_FOUNDRY_DEPLOYMENT"):
        monkeypatch.delenv(name, raising=False)
    response = client.post("/ask", json={"question": "How do I request leave?"})
    assert response.status_code == 503
