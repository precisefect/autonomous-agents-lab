# Agent Template

Blueprint FastAPI service for autonomous industrial AI agents in manufacturing environments.

## Architecture

```
app/
├── api/          # HTTP routes (FastAPI routers)
├── services/     # Business logic and orchestration
├── models/       # ML model wrappers
├── core/         # Domain rules (extend per agent)
└── utils/        # Logging, configuration
```

Data flows: **API → Service → Model → Response**

## Setup

```bash
cd agent-template
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
```

## Run Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Shared core

`app/utils/paths.py` adds the lab `shared-core/` directory to `PYTHONPATH` at startup.
New agents created via `create-agent` scripts receive a bundled `shared-core/` copy for Docker.

## Run with Docker

From the **lab root** (template):

```bash
docker build -f agent-template/Dockerfile -t agent-template .
docker run -p 8000:8000 --env-file agent-template/.env agent-template
```

From a **generated agent** folder (e.g. `agents/quality-inspector`):

```bash
docker build -t quality-inspector .
docker run -p 8000:8000 --env-file .env quality-inspector
```

## API Usage

**Health**

```bash
curl http://localhost:8000/health
```

**Predict**

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"temperature": 72.5, "pressure": 14.2, "vibration": 0.03}}'
```

Example response:

```json
{
  "prediction": 0.4312,
  "status": "success",
  "agent": "agent-template",
  "metadata": {
    "threshold": 0.5,
    "alert": false,
    "field_count": 3
  }
}
```

## Testing

```bash
python -m unittest discover -s tests -v
```

## Extending

1. Replace `DummyModel` in `app/models/model.py` with your trained model.
2. Add domain logic in `app/services/agent_service.py`.
3. Register new routes in `app/api/routes.py`.
4. Use `shared-core/` modules for data loading, anomaly detection, and alerts.

## Environment Variables

See `.env.example` for all supported settings.
