from contextlib import AsyncExitStack
from typing import Any

from mcp.client import Transport as MCPTransport
from mcp.client.stdio import StdioServerParameters
from pydantic import BaseModel, Field

from .._types.transport import Transport

type ClientTarget = StdioServerParameters | MCPTransport


class BaseConnection(BaseModel):
    transport: Transport = Field(frozen=True)
    session_kwargs: dict[str, Any] = Field(default_factory=dict)

    async def enter_client_target(self, stack: AsyncExitStack) -> ClientTarget:
        """Build what `mcp.Client` connects to.

        Anything that must outlive the session (such as an HTTP client) is
        registered on `stack`, which the session owner closes on disconnect.
        """
        raise NotImplementedError  # pragma: no cover
