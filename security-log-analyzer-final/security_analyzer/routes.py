from datetime import datetime, timezone
from flask import Blueprint, current_app, jsonify, request
from .services.classifier import classify_log
from .services.event_store import load_events

api = Blueprint("api", __name__, url_prefix="/api")
VALID_SEVERITIES = {"critical", "high", "medium", "low", "info"}


@api.get("/health")
def health():
    return jsonify(status="ok", mode="local demo")


@api.get("/events")
def events():
    rows = load_events(current_app.config["DATA_FILE"])
    severity = request.args.get("severity", "all").strip().lower()
    query = request.args.get("q", "").strip().lower()

    if severity not in VALID_SEVERITIES | {"all"}:
        return jsonify(error="Unsupported severity filter."), 400
    if len(query) > 200:
        return jsonify(error="Search query must be 200 characters or fewer."), 400

    if severity != "all":
        rows = [row for row in rows if str(row.get("severity", "info")).lower() == severity]
    if query:
        rows = [row for row in rows if query in str(row).lower()]

    rows.sort(key=lambda row: str(row.get("timestamp", "")), reverse=True)
    total = len(rows)
    try:
        limit = min(max(int(request.args.get("limit", 100)), 1), 500)
        offset = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        return jsonify(error="limit and offset must be integers."), 400

    return jsonify(events=rows[offset:offset + limit], total=total, limit=limit, offset=offset)


@api.get("/summary")
def summary():
    rows = load_events(current_app.config["DATA_FILE"])
    counts = {
        key: sum(str(row.get("severity", "info")).lower() == key for row in rows)
        for key in ("critical", "high", "medium", "low", "info")
    }
    return jsonify(total=len(rows), **counts)


@api.post("/analyze")
def analyze():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json."), 415
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error="Request body must be a JSON object."), 400

    raw_log = body.get("log")
    if not isinstance(raw_log, str):
        return jsonify(error="The 'log' field must be a string."), 400
    line = raw_log.strip()
    if not line:
        return jsonify(error="Paste a log line to analyze."), 400
    if len(line) > 5000:
        return jsonify(error="Keep the log sample under 5,000 characters."), 400

    severity, explanation = classify_log(line)
    return jsonify(
        severity=severity,
        explanation=explanation,
        analyzed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        disclaimer="Keyword-based educational demo, not a definitive security verdict."
    )
