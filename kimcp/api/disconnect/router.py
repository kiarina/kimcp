from fastapi import APIRouter, HTTPException

from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import mcp_server_registry

router = APIRouter()


@router.delete("/agents/{agent_id}/mcp-servers/{server_name}")
async def disconnect(agent_id: AgentID, server_name: str) -> dict:
    server = mcp_server_registry.get(agent_id=agent_id, server_name=server_name)
    if server is None:
        raise HTTPException(status_code=404, detail="Connection not found.")

    client = mcp_client_registry.ensure(agent_id)
    await client.disconnect(server_name)
    mcp_server_registry.delete(agent_id=agent_id, server_name=server_name)

    return {
        "agent_id": agent_id,
        "server_name": server_name,
        "disconnected": True,
    }
