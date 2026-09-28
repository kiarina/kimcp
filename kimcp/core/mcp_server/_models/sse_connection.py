from contextlib import AsyncExitStack
from typing import Any, Literal

from mcp.client.sse import sse_client
from pydantic import Field

from .base_connection import BaseConnection, ClientTarget

DEFAULT_TIMEOUT = 5.0
DEFAULT_SSE_READ_TIMEOUT = 300.0


class SSEConnection(BaseConnection):
    transport: Literal["sse"] = "sse"
    url: str
    headers: dict[str, Any] = Field(default_factory=dict)
    timeout: float | None = None
    sse_read_timeout: float | None = None

    async def enter_client_target(self, stack: AsyncExitStack) -> ClientTarget:
        return sse_client(
            self.url,
            headers=self.headers,
            timeout=self.timeout if self.timeout is not None else DEFAULT_TIMEOUT,
            sse_read_timeout=(
                self.sse_read_timeout
                if self.sse_read_timeout is not None
                else DEFAULT_SSE_READ_TIMEOUT
            ),
        )
