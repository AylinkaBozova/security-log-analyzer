# Sentinel — Security Log Analyzer

A lightweight Flask application for exploring security events and classifying sample log lines with transparent, keyword-based rules. Includes a responsive dashboard, JSON API, input validation, security headers, and automated tests.

> **Important:** This is an educational demo, not a production SIEM or an automated incident-response system. Keyword matches can produce false positives and false negatives. Always validate findings against surrounding telemetry.

## Features

- Dashboard with severity summary and searchable/filterable event stream.
- Rule-based classification across `critical`, `high`, `medium`, `low`, and `info`.
- JSON endpoints for health, event listing, summary, and log analysis.
- Bounded result pagination and request-size/input validation.
- Security headers and safe text rendering in the frontend.
- Modular application factory and pytest test suite.

## Technology

- Python 3.10+
- Flask 3
- HTML5, CSS, vanilla JavaScript
- Pytest

GPU rendering libraries such as Three.js/PixiJS are intentionally not included: this application renders a conventional data dashboard and does not have a particle/graphics workload that benefits from GPU scene rendering. The frontend uses small, event-driven updates and avoids a per-frame animation loop.

## Project structure

```text
security-log-analyzer/
├── app.py
├── security_analyzer/
│   ├── __init__.py
│   ├── config.py
│   ├── routes.py
│   ├── web.py
│   └── services/
│       ├── classifier.py
│       └── event_store.py
├── data/
│   └── events.json
├── templates/
│   └── index.html
├── static/
│   ├── css/styles.css
│   └── js/app.js
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_classifier.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/security-log-analyzer.git
cd security-log-analyzer
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Run tests

```bash
pytest
```

## API reference

### `GET /api/health`

Returns application status.

### `GET /api/summary`

Returns total events and counts by severity.

### `GET /api/events`

Supported query parameters:

| Parameter | Description |
|---|---|
| `severity` | `all`, `critical`, `high`, `medium`, `low`, or `info` |
| `q` | Case-insensitive search, up to 200 characters |
| `limit` | Page size, 1–500 (default 100) |
| `offset` | Number of matching records to skip (default 0) |

Example:

```bash
curl "http://127.0.0.1:5000/api/events?severity=high&limit=25&offset=0"
```

### `POST /api/analyze`

Request:

```json
{
  "log": "Multiple failed logins detected for admin"
}
```

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"log":"ransomware detected"}'
```

The endpoint accepts a non-empty string up to 5,000 characters.

## Configuration

- `PORT`: HTTP port (default `5000`).
- `SECURITY_ANALYZER_DATA`: optional path to the JSON event dataset.
- `SECRET_KEY`: Flask secret key. Set a strong random value when deploying.

Example:

```bash
export SECRET_KEY="replace-with-a-long-random-secret"
export SECURITY_ANALYZER_DATA="/path/to/events.json"
python app.py
```

## Data format

`data/events.json` must contain a JSON array. Each event may include:

```json
{
  "severity": "high",
  "message": "Multiple failed logins",
  "source": "203.0.113.42",
  "timestamp": "2026-10-16T08:31:00Z"
}
```

The included JSON store is suitable for a local demo. For concurrent users or production workloads, replace it with a database and add authentication, authorization, audit logging, monitoring, and managed secret storage.

## Deployment

The Flask backend requires a Python-capable host (for example, Render, Railway, or a VPS); GitHub Pages cannot host the dynamic Flask API. Configure the host's start command as:

```bash
gunicorn 'security_analyzer:create_app()'
```

Add `gunicorn` to `requirements.txt` for that deployment. Configure a persistent volume/database for event data: ephemeral filesystems may reset on redeploy. Set `SECRET_KEY` and `SECURITY_ANALYZER_DATA` through the hosting provider's environment settings.

A live demo URL should be added here after deployment:

**Live demo:** _Not deployed yet._

## Development standards

- Keep routes thin; put classification and storage logic in `services/`.
- Add a test for every new rule and API behavior.
- Run `pytest` before pushing changes.
- Do not commit credentials, `.env` files, or real sensitive log data.

## License

Choose and add a license before publishing this repository publicly.
