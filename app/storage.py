import json
from pathlib import Path
from typing import Dict, Any, List

DATA_FILE = Path('data/data.json')

def _init_storage() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open('w') as f:
            json.dump({'users': []}, f)

def load_data() -> Dict[str, Any]:
    _init_storage()
    with DATA_FILE.open() as f:
        return json.load(f)

def save_data(data: Dict[str, Any]) -> None:
    _init_storage()
    with DATA_FILE.open('w') as f:
        json.dump(data, f)
