import json
import pytest
from security_analyzer import create_app


@pytest.fixture()
def app(tmp_path):
    data_file = tmp_path / "events.json"
    data_file.write_text(json.dumps([
        {"severity": "critical", "message": "Malware confirmed", "timestamp": "2026-01-01T00:00:00Z"},
        {"severity": "high", "message": "Multiple failed logins", "timestamp": "2026-01-02T00:00:00Z"},
        {"severity": "info", "message": "Backup completed", "timestamp": "2026-01-03T00:00:00Z"}
    ]), encoding="utf-8")
    app = create_app({"TESTING": True, "DATA_FILE": data_file})
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
