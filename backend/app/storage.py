import json
from pathlib import Path
from typing import Any

DATA_DIR = Path("/data")
DATA_FILE = DATA_DIR / "data.json"


def read_data() -> Any:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def write_data(data: Any) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f)
