from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Check that health endpoint returns 200 OK."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_rag_index():
    """Verify that /rag/index accepts data and returns valid response."""
    response = client.post("/rag/index", data={"content": "FastAPI test document"})
    assert response.status_code == 200
    assert "status" in response.json()
