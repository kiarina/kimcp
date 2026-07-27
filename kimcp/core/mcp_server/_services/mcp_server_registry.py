import threading

from kimcp.core.app import AgentID

from .._models.mcp_server import MCPServer
from .._types.server_name import ServerName


class _MCPServerRegistry:
    def __init__(self) -> None:
        self._registry: dict[AgentID, dict[ServerName, MCPServer]] = {}
        self._lock = threading.Lock()

    def register(self, *, agent_id: AgentID, server: MCPServer) -> None:
        with self._lock:
            self._registry.setdefault(agent_id, {})[server.server_name] = server

    def get(
        self,
        *,
        agent_id: AgentID,
        server_name: ServerName,
    ) -> MCPServer | None:
        with self._lock:
            return self._registry.get(agent_id, {}).get(server_name)

    def list(self, *, agent_id: AgentID) -> list[MCPServer]:
        with self._lock:
            return list(self._registry.get(agent_id, {}).values())

    def clear(self) -> None:
        with self._lock:
            self._registry.clear()

    def delete(self, *, agent_id: AgentID, server_name: ServerName) -> None:
        with self._lock:
            agent_registry = self._registry.get(agent_id)
            if not agent_registry:
                return

            agent_registry.pop(server_name, None)

            if not agent_registry:
                self._registry.pop(agent_id, None)


mcp_server_registry = _MCPServerRegistry()

__all__ = ["mcp_server_registry"]
