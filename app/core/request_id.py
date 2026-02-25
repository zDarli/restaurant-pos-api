# app/core/request_id.py
from __future__ import annotations

import contextvars

request_id_ctx_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)


def get_request_id() -> str | None:
    return request_id_ctx_var.get()


def set_request_id(value: str | None) -> None:
    request_id_ctx_var.set(value)
