# app/core/exception_handlers.py
from __future__ import annotations

import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError
from app.core.request_id import get_request_id
from app.core.config import get_settings

logger = logging.getLogger("app.errors")


def error_payload(*, code: str, message: str, details=None) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "request_id": get_request_id() or "-",
    }


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # AppError — ожидаемые бизнес/доменные ошибки
    logger.info(
        "app_error",
        extra={
            "code": exc.code,
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(code=exc.code, message=exc.message, details=exc.details),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    # HTTPException — ошибки типа 404/403/401 и т.п.
    logger.info(
        "http_error",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(code="HTTP_ERROR", message=str(exc.detail)),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Ошибки валидации pydantic на входе
    logger.info(
        "validation_error",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": exc.errors(),
        },
    )
    return JSONResponse(
        status_code=422,
        content=error_payload(code="VALIDATION_ERROR", message="Invalid request", details=exc.errors()),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    settings = get_settings()

    # Неожиданные ошибки — логируем как error/exception
    logger.exception(
        "unhandled_error",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    # Клиенту НИКОГДА traceback, максимум — нейтральное сообщение
    message = "Internal server error"

    # В debug можно показать чуть больше (но всё равно без traceback)
    if settings.DEBUG:
        message = "Internal server error (debug mode)"

    return JSONResponse(
        status_code=500,
        content=error_payload(code="INTERNAL_ERROR", message=message),
    )