from fastapi import APIRouter, HTTPException

from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import MCPServer, mcp_server_registry

router = APIRouter()


@router.post("/agents/{agent_id}/mcp-servers")
async def connect(agent_id: AgentID, server: MCPServer) -> dict:
    client = mcp_client_registry.ensure(agent_id=agent_id)
    try:
        await client.connect(server)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to MCP server {server.server_name}: {exc}",
        ) from exc

    mcp_server_registry.register(agent_id=agent_id, server=server)

    return {
        "agent_id": agent_id,
        "mcp_server": server.model_dump(mode="json"),
    }
