# Autonomous Agents Lab

Production-ready **Agent Factory** for building, testing, and deploying multiple autonomous industrial AI agents focused on manufacturing use cases.

## Overview

This monorepo provides:

- **agent-template** — Scaffold for new FastAPI-based agents with clean architecture layers
- **shared-core** — Reusable data loading, anomaly detection, and alerting modules
- **agents/** — Per-agent deployments created from the template
- **scripts/** — Automation to spin up new agents quickly
- **datasets/** — Shared manufacturing datasets and references

## Folder Structure

```
autonomous-agents-lab/
├── agent-template/       # Blueprint for new agents
├── shared-core/          # Shared industrial AI utilities
├── datasets/             # Shared data assets
├── scripts/              # Automation (create-agent.sh)
└── agents/               # Generated agent instances
```

## Quick Start

### Prerequisites

- Python 3.10+
- Git
- Docker (optional, for containerized runs)

### Sample agent

`agents/quality-inspector/` is a ready-made example with `shared-core` bundled.

### Create a New Agent

From the repository root:

```bash
./scripts/create-agent.sh quality-inspector
```

On Windows (PowerShell):

```powershell
.\scripts\create-agent.ps1 -AgentName quality-inspector
```

Or Git Bash / WSL:

```bash
bash scripts/create-agent.sh quality-inspector
```

### Shared core integration

Agents load `shared-core` automatically via `app/utils/paths.py` (walks up the lab tree or uses a bundled `shared-core/` folder). The `create-agent` scripts copy `shared-core` into each new agent for Docker and standalone deploys.

### Run an Agent Locally

```bash
cd agents/quality-inspector   # or agent-template for the blueprint
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run with Docker

Template (from lab root):

```bash
docker build -f agent-template/Dockerfile -t agent-template .
```

Generated agent:

```bash
cd agents/quality-inspector
docker build -t quality-inspector .
docker run -p 8001:8000 quality-inspector
```

**Windows note:** If `pip install` fails with long-path errors, clone the repo to a shorter path (e.g. `C:\dev\agents-lab`) or enable [Windows long paths](https://pip.pypa.io/warnings/enable-long-paths).

### Example API Calls

Health check:

```bash
curl http://localhost:8000/health
```

Prediction:

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"temperature": 72.5, "pressure": 14.2, "vibration": 0.03}}'
```

### Run Tests

```bash
cd agent-template
python -m unittest discover -s tests -v
```

## Development Workflow

1. Prototype in `agent-template/notebooks/`
2. Implement logic in `app/services/` and `app/models/`
3. Expose endpoints via `app/api/routes.py`
4. Copy to `agents/<name>` with `create-agent.sh`
5. Deploy with Docker or your orchestration platform

## Git (monorepo)

This lab is a single repository. All agents under `agents/` are tracked together.

```powershell
cd autonomous-agents-lab
git status
git add .
git commit -m "Your message"
```

### Connect a new remote (GitHub, Azure DevOps, etc.)

After creating an empty repository on your host:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_ORG/autonomous-agents-lab.git
git push -u origin main
```

New agents: run `create-agent`, then `git add agents/<name>` and commit from the lab root.

## License

Internal use — adjust per your organization.
