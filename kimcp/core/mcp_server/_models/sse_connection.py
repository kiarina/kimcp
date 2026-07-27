from typing import Any, Literal

from pydantic import Field

from .base_connection import BaseConnection


class SSEConnection(BaseConnection):
    transport: Literal["sse"] = "sse"
    url: str
    headers: dict[str, Any] = Field(default_factory=dict)
    timeout: float | None = None
    sse_read_timeout: float | None = None
