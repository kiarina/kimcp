from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Any

from kimcp.core.mcp_server import MCPServer


@dataclass
class MCPSession:
    server: MCPServer
    context_manager: AbstractAsyncContextManager[Any]
    session: Any
