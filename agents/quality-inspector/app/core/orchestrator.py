"""Domain orchestration hooks — extend with state machines, schedules, or PLC integrations."""

from typing import Any


def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    """
    Placeholder input validation for manufacturing payloads.
    Enforce schemas, ranges, and required sensor keys per agent.
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary")
    return data
