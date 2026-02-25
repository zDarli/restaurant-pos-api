from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers import health
from app.core.config import get_settings
from app.core.errors import AppError
from app.core.exception_handlers import (
    app_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware

setup_logging()

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(health.router)
