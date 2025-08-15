import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app, missions, Mission, Position

client = TestClient(app)


def setup_function(_):
    missions.clear()


def test_assign_ok_then_capacity_exceeded_422():
    missions[1] = Mission(id=1, positions=[Position(label="pilot", count=1)])

    res1 = client.post("/missions/1/assign", json={"role_label": "pilot", "user_id": 1})
    assert res1.status_code == 200, res1.text

    res2 = client.post("/missions/1/assign", json={"role_label": "pilot", "user_id": 2})
    assert res2.status_code == 422
    assert "capacity" in res2.json()["detail"]


def test_assign_invalid_role_422():
    missions[1] = Mission(id=1, positions=[Position(label="pilot", count=1)])

    res = client.post("/missions/1/assign", json={"role_label": "copilot", "user_id": 1})
    assert res.status_code == 422
    assert "Invalid role" in res.json()["detail"]
