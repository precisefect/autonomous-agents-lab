"""FastAPI entry point for the industrial AI agent."""

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.utils.paths import ensure_shared_core_on_path

# Lab-wide utilities (data_loader, anomaly_detection, alerting)
ensure_shared_core_on_path()

app = FastAPI(
    title="Industrial AI Agent",
    description="Autonomous agent template for manufacturing use cases",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict:
    """Liveness/readiness probe for orchestrators and load balancers."""
    return {"status": "healthy", "service": "agent-template"}


app.include_router(api_router, prefix="/api/v1", tags=["agent"])
