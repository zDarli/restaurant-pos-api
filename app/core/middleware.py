# app/core/middleware.py
from __future__ import annotations

import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_id import set_request_id

logger = logging.getLogger("app.http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        set_request_id(rid)

        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            # даём FastAPI обработать исключение через глобальные handlers
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-ID"] = rid

        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )

        return response