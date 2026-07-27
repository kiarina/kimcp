from typing import Any, Literal

from pydantic import Field

from .base_connection import BaseConnection


class StreamableHTTPConnection(BaseConnection):
    transport: Literal["streamable_http"] = "streamable_http"
    url: str
    headers: dict[str, Any] = Field(default_factory=dict)
    timeout: float | None = None
    sse_read_timeout: float | None = None
    terminate_on_close: bool | None = None
