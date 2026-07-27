from typing import Any, cast

from langchain_mcp_adapters.sessions import (
    Connection,
    SSEConnection,
    StdioConnection,
    StreamableHttpConnection,
)
from pydantic import BaseModel, Field

from .._types.transport import Transport


class BaseConnection(BaseModel):
    transport: Transport = Field(frozen=True)
    session_kwargs: dict[str, Any] = Field(default_factory=dict)

    def to_connection(self) -> Connection:
        connection = {k: v for k, v in self.model_dump().items() if v is not None}

        if self.transport == "sse":
            return cast(SSEConnection, connection)
        elif self.transport == "stdio":
            return cast(StdioConnection, connection)
        elif self.transport == "streamable_http":
            return cast(StreamableHttpConnection, connection)
        else:  # pragma: no cover
            raise AssertionError(f"Unsupported transport: {self.transport}")
