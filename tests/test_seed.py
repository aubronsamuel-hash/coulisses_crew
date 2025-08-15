import json
import subprocess
import sys
from pathlib import Path

def run_seed(users=2, missions=3, days=2):
    cmd = [sys.executable, 'scripts/seed_plus.py', '--reset', '--users', str(users), '--missions', str(missions), '--days', str(days), '--all']
    subprocess.run(cmd, check=True)

def load():
    with open('data/data.json') as f:
        return json.load(f)

def test_seed_inserts_consistent_ids():
    run_seed()
    first = load()
    run_seed()
    second = load()
    assert [u['id'] for u in first['users']] == [u['id'] for u in second['users']]
    assert [m['id'] for m in first['missions']] == [m['id'] for m in second['missions']]
    assert [a['id'] for a in first['assignments']] == [a['id'] for a in second['assignments']]
    # cleanup
    Path('data/data.json').unlink()
