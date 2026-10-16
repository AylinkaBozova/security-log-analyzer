def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_summary_counts_events(client):
    response = client.get("/api/summary")
    assert response.json == {"total": 3, "critical": 1, "high": 1, "medium": 0, "low": 0, "info": 1}


def test_event_filter_and_search(client):
    response = client.get("/api/events?severity=high")
    assert response.status_code == 200
    assert response.json["total"] == 1
    assert response.json["events"][0]["severity"] == "high"


def test_invalid_severity_is_rejected(client):
    assert client.get("/api/events?severity=unknown").status_code == 400


def test_analyze_log(client):
    response = client.post("/api/analyze", json={"log": "ransomware detected"})
    assert response.status_code == 200
    assert response.json["severity"] == "critical"
    assert "disclaimer" in response.json


def test_analyze_requires_string(client):
    assert client.post("/api/analyze", json={"log": 123}).status_code == 400


def test_analyze_rejects_empty_and_oversized_logs(client):
    assert client.post("/api/analyze", json={"log": "  "}).status_code == 400
    assert client.post("/api/analyze", json={"log": "x" * 5001}).status_code == 400


def test_analyze_requires_json_content_type(client):
    assert client.post("/api/analyze", data="hello").status_code == 415


def test_security_headers_are_set(client):
    response = client.get("/api/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in response.headers
