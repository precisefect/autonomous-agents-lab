"""Centralized logging configuration."""

import logging
import sys

from app.utils.config import get_settings


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
