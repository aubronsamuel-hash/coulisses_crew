import sys
from pathlib import Path
from fastapi.testclient import TestClient

# add backend to path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
