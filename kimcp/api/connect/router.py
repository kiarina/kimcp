from fastapi import APIRouter

from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import MCPServer, mcp_server_registry

router = APIRouter()


@router.post("/agents/{agent_id}/mcp-servers")
async def connect(agent_id: AgentID, server: MCPServer) -> dict:
    mcp_server_registry.register(agent_id=agent_id, server=server)
    client = mcp_client_registry.ensure(agent_id=agent_id)
    await client.connect(server)

    return {
        "agent_id": agent_id,
        "mcp_server": server.model_dump(mode="json"),
    }
