from fastapi.testclient import TestClient
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)


def sample_mission():
    return {
        "title": "Sample",
        "start": "2023-01-01T10:00:00",
        "end": "2023-01-01T12:00:00",
        "location": "HQ",
        "status": "draft",
        "positions": [
            {"label": "medic", "count": 2, "skills": {"first_aid": "advanced"}}
        ],
    }


def test_create_list_update_delete_ok():
    payload = sample_mission()
    resp = client.post("/missions", json=payload)
    assert resp.status_code == 201
    mission = resp.json()
    assert mission["id"] == 1

    resp = client.get("/missions")
    assert resp.status_code == 200
    missions = resp.json()
    assert len(missions) == 1

    update = payload.copy()
    update["title"] = "Updated"
    resp = client.put("/missions/1", json=update)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"

    resp = client.delete("/missions/1")
    assert resp.status_code == 204
    resp = client.get("/missions")
    assert resp.json() == []


def test_create_invalid_dates_422():
    payload = sample_mission()
    payload["end"] = payload["start"]
    resp = client.post("/missions", json=payload)
    assert resp.status_code == 422
