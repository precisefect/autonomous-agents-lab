# Quality Inspector Agent

Sample manufacturing agent generated from `agent-template`, with `shared-core` bundled for standalone and Docker runs.

## Quick start

```powershell
cd agents/quality-inspector
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Docker

```powershell
docker build -t quality-inspector .
docker run -p 8001:8000 quality-inspector
```

## API

```bash
curl http://localhost:8001/health
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d "{\"data\": {\"temperature\": 85.0, \"pressure\": 18.5, \"vibration\": 0.08}}"
```

Enable alerting in `.env`:

```
ALERT_ENABLED=true
PREDICTION_THRESHOLD=0.3
```
