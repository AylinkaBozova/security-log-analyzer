"""Small JSON-backed event store. Replace with a database for multi-user production use."""
import json
from pathlib import Path


def load_events(data_file) -> list:
    path = Path(data_file)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]
