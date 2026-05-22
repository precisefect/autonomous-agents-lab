"""Agent orchestration — coordinates model inference and response shaping."""

from typing import Any

from app.core.orchestrator import validate_input
from app.models.model import DummyModel
from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.utils.paths import ensure_shared_core_on_path

ensure_shared_core_on_path()

import alerting  # noqa: E402  # shared-core on sys.path

logger = get_logger(__name__)
_model = DummyModel()


def run_agent(data: dict[str, Any]) -> dict[str, Any]:
    """
    Execute the agent pipeline on incoming manufacturing data.

    Args:
        data: Sensor or process readings as key-value pairs.

    Returns:
        Prediction payload with status and agent identifier.
    """
    settings = get_settings()
    payload = validate_input(data)
    logger.info("Running agent '%s' with %d fields", settings.app_name, len(payload))

    prediction = _model.predict(payload)
    threshold = settings.prediction_threshold
    is_alert = prediction >= threshold

    if is_alert and settings.alert_enabled:
        alerting.alert_on_threshold(
            value=prediction,
            threshold=threshold,
            source=settings.app_name,
            webhook_url=settings.alert_webhook_url or None,
        )

    return {
        "prediction": prediction,
        "status": "success",
        "agent": settings.app_name,
        "metadata": {
            "threshold": threshold,
            "alert": is_alert,
            "field_count": len(payload),
        },
    }
