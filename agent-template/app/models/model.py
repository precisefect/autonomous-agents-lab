"""Placeholder model for development and integration tests."""

from typing import Any


class DummyModel:
    """
    Stand-in model until a trained sklearn or custom model is wired in.
    Uses a deterministic hash of numeric inputs for reproducible mock scores.
    """

    def predict(self, data: dict[str, Any]) -> float:
        """Return a mock anomaly/risk score in [0, 1]."""
        if not data:
            return 0.0

        numeric_values = [
            float(v)
            for v in data.values()
            if isinstance(v, (int, float))
        ]
        if not numeric_values:
            return 0.25

        score = sum(numeric_values) / len(numeric_values)
        # Normalize to a simple 0–1 range for demo purposes
        normalized = abs(score % 100) / 100.0
        return round(min(max(normalized, 0.0), 1.0), 4)
