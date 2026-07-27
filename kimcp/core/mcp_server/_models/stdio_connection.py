from typing import Literal

from pydantic import Field

from .base_connection import BaseConnection


class StdioConnection(BaseConnection):
    transport: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    cwd: str | None = None
    encoding: str | None = None
