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
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
                "filters": ["request_id"],
            }
        },
        "filters":{
            "request_id": {"()": "app.core.logging_filters.RequestIdFilter"}
        },
        "root": {  # root-логгер — базовый для всего приложения
            "handlers": ["console"],
            "level": level,
        },
        "loggers": {
            # можно управлять шумом библиотек
            "uvicorn.error": {"level": level, "propagate": True},
            "uvicorn.access": {"level": level, "propagate": True},
            "sqlalchemy.engine": {"level": "WARNING", "propagate": True},
        },
    }

    logging.config.dictConfig(logging_config)