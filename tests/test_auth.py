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


def register_and_login(username: str, password: str) -> str:
    resp = client.post('/auth/register', json={'username': username, 'password': password})
    assert resp.status_code == 200
    resp = client.post('/auth/token-json', json={'username': username, 'password': password})
    assert resp.status_code == 200
    return resp.json()['access_token']

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


def test_notify_test_dry_run_ok():
    os.environ['NOTIFY_DRY_RUN'] = '1'
    token = register_and_login('bob', 'builder')
    resp = client.post('/auth/me/notify-test', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['dry_run'] is True


def test_prefs_upsert_ok():
    token = register_and_login('charlie', 'password')
    resp = client.put(
        '/auth/me/prefs',
        json={'email': 'charlie@example.com'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert resp.status_code == 200
    assert resp.json()['email'] == 'charlie@example.com'

    resp = client.put(
        '/auth/me/prefs',
        json={'telegram': '@charlie'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert resp.status_code == 200
    prefs = resp.json()
    assert prefs['email'] == 'charlie@example.com'
    assert prefs['telegram'] == '@charlie'
