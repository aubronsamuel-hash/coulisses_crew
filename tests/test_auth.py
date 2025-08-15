import os
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient

from app.main import app


# ensure a clean data directory for tests
if os.path.exists('data'):
    shutil.rmtree('data')

client = TestClient(app)

def test_register_then_login_me():
    resp = client.post('/auth/register', json={'username': 'alice', 'password': 'wonderland'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['username'] == 'alice'
    assert data['role'] == 'intermittent'

    resp = client.post('/auth/token-json', json={'username': 'alice', 'password': 'wonderland'})
    assert resp.status_code == 200
    token = resp.json()['access_token']

    resp = client.get('/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    profile = resp.json()
    assert profile['username'] == 'alice'
    assert profile['role'] == 'intermittent'
