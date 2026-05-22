"""Application settings loaded from environment variables."""

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the agent service."""

    app_name: str
    log_level: str
    api_host: str
    api_port: int
    model_path: str
    prediction_threshold: float
    alert_webhook_url: str
    alert_enabled: bool


@lru_cache
def get_settings() -> Settings:
    """Load and cache settings from the environment."""
    return Settings(
        app_name=os.getenv("APP_NAME", "agent-template"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        api_host=os.getenv("API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("API_PORT", "8000")),
        model_path=os.getenv("MODEL_PATH", "data/models/dummy.pkl"),
        prediction_threshold=float(os.getenv("PREDICTION_THRESHOLD", "0.5")),
        alert_webhook_url=os.getenv("ALERT_WEBHOOK_URL", ""),
        alert_enabled=os.getenv("ALERT_ENABLED", "false").lower() == "true",
    )
