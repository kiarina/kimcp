from contextlib import AsyncExitStack
from typing import Any, Literal

import httpx2
from mcp.client.streamable_http import streamable_http_client
from pydantic import Field

from .base_connection import BaseConnection, ClientTarget

DEFAULT_TIMEOUT = 30.0
DEFAULT_SSE_READ_TIMEOUT = 300.0


class StreamableHTTPConnection(BaseConnection):
    transport: Literal["streamable_http"] = "streamable_http"
    url: str
    headers: dict[str, Any] = Field(default_factory=dict)
    timeout: float | None = None
    sse_read_timeout: float | None = None
    terminate_on_close: bool | None = None

    async def enter_client_target(self, stack: AsyncExitStack) -> ClientTarget:
        # The transport leaves a caller-provided HTTP client open, so the stack closes it.
        http_client = await stack.enter_async_context(
            httpx2.AsyncClient(
                headers=self.headers,
                timeout=httpx2.Timeout(
                    self.timeout if self.timeout is not None else DEFAULT_TIMEOUT,
                    read=(
                        self.sse_read_timeout
                        if self.sse_read_timeout is not None
                        else DEFAULT_SSE_READ_TIMEOUT
                    ),
                ),
            )
        )

        return streamable_http_client(
            self.url,
            http_client=http_client,
            terminate_on_close=(
                self.terminate_on_close if self.terminate_on_close is not None else True
            ),
        )
