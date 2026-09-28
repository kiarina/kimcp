from contextlib import AsyncExitStack
from typing import Literal

from mcp.client.stdio import StdioServerParameters
from pydantic import Field

from .base_connection import BaseConnection, ClientTarget


class StdioConnection(BaseConnection):
    transport: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    cwd: str | None = None
    encoding: str | None = None

    async def enter_client_target(self, stack: AsyncExitStack) -> ClientTarget:
        params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env or None,
            cwd=self.cwd,
        )
        if self.encoding is not None:
            params.encoding = self.encoding

        return params
