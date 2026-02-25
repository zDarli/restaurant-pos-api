from __future__ import annotations

import logging
import logging.config
from typing import Any

from app.core.config import get_settings


def setup_logging() -> None:
    """
    Настраивает logging для приложения.
    Вызывается один раз при старте (в app/main.py).
    """
    settings = get_settings()
    level = settings.LOG_LEVEL.upper()

    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s | %(levelname)s | %(name)s | "
                    "rid=%(request_id)s | %(message)s"
                )
            },
        },
        "filters": {
            "request_id": {"()": "app.core.logging_filters.RequestIdFilter"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "default",
                "filters": ["request_id"],
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": level,
            "handlers": ["console"],
        },
        "loggers": {
            "app.http": {"level": level, "propagate": True},
            "app.errors": {"level": level, "propagate": True},
            "uvicorn.error": {"level": level, "propagate": True},
            "uvicorn.access": {"level": level, "propagate": True},
            "sqlalchemy.engine": {"level": "WARNING", "propagate": True},
        },
    }

    try:
        logging.config.dictConfig(logging_config)
    except Exception:
        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
        logging.getLogger("app.logging").exception(
            "Failed to configure logging via dictConfig"
        )
