"""API routes for agent inference and operations."""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.agent_service import run_agent

router = APIRouter()


class PredictRequest(BaseModel):
    """Incoming sensor or process data for inference."""

    data: dict[str, Any] = Field(
        ...,
        description="Key-value payload (e.g. temperature, pressure, vibration)",
        examples=[{"temperature": 72.5, "pressure": 14.2, "vibration": 0.03}],
    )


class PredictResponse(BaseModel):
    """Structured agent response."""

    prediction: float
    status: str
    agent: str
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> dict[str, Any]:
    """
    Run the agent pipeline on input data and return a mock prediction.
    Replace service logic with real models per manufacturing use case.
    """
    return run_agent(request.data)
