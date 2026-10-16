import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "local-demo-change-this-key")
    MAX_CONTENT_LENGTH = 16 * 1024
    JSON_SORT_KEYS = False
    DATA_FILE = Path(os.environ.get(
        "SECURITY_ANALYZER_DATA",
        Path(__file__).resolve().parent.parent / "data" / "events.json"
    ))
