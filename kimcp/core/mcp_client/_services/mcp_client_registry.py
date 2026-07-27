import threading

from kimcp.core.app import AgentID

from .._models.mcp_client import MCPClient

_registry: dict[AgentID, MCPClient] = {}
_lock = threading.Lock()


def ensure(agent_id: AgentID) -> MCPClient:
    with _lock:
        if agent_id not in _registry:
            _registry[agent_id] = MCPClient(agent_id=agent_id)

        return _registry[agent_id]


async def close_all() -> None:
    with _lock:
        clients = list(_registry.values())

    for client in clients:
        await client.disconnect_all()

    with _lock:
        _registry.clear()
