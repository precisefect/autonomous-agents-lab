"""Placeholder alerting utilities for manufacturing incidents."""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib import request
from urllib.error import URLError

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Structured alert payload for MES/SCADA integrations."""

    severity: str
    message: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "message": self.message,
            "source": self.source,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


def send_alert(alert: Alert, webhook_url: str | None = None) -> bool:
    """
    Dispatch an alert. Logs locally; posts to webhook when URL is provided.

    Returns:
        True if delivery succeeded (or log-only mode), False on HTTP failure.
    """
    payload = alert.to_dict()
    logger.warning("ALERT [%s] %s: %s", alert.severity, alert.source, alert.message)

    if not webhook_url:
        return True

    try:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except URLError as exc:
        logger.error("Failed to send alert: %s", exc)
        return False


def alert_on_threshold(
    value: float,
    threshold: float,
    source: str,
    webhook_url: str | None = None,
) -> Alert | None:
    """Create and optionally send an alert when a metric exceeds threshold."""
    if value < threshold:
        return None

    alert = Alert(
        severity="high",
        message=f"Metric {value:.4f} exceeded threshold {threshold:.4f}",
        source=source,
        metadata={"value": value, "threshold": threshold},
    )
    send_alert(alert, webhook_url=webhook_url)
    return alert
