from fastapi import APIRouter

from kimcp.core.app import AgentID
from kimcp.core.mcp_server import mcp_server_registry

router = APIRouter()


@router.get("/agents/{agent_id}/mcp-servers")
async def list_mcp_servers(agent_id: AgentID) -> dict:
    return {
        "agent_id": agent_id,
        "mcp_servers": [
            server.model_dump(mode="json") for server in mcp_server_registry.list(agent_id=agent_id)
        ],
    }
