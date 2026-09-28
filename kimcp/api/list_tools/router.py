from typing import Any

from fastapi import APIRouter, HTTPException
from mcp.types import Tool

from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import ServerName, mcp_server_registry

router = APIRouter()


@router.get("/agents/{agent_id}/mcp-servers/{server_name}/tools")
async def list_mcp_server_tools(
    agent_id: AgentID,
    server_name: str,
) -> dict[str, Any]:
    server = mcp_server_registry.get(agent_id=agent_id, server_name=server_name)
    if server is None:
        raise HTTPException(status_code=404, detail="MCP Server not found.")

    client = mcp_client_registry.ensure(agent_id=agent_id)

    try:
        tools = await client.list_tools([server_name])
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "agent_id": agent_id,
        "tools": [_tool_to_dict(tool_server_name, tool) for tool_server_name, tool in tools],
    }


def _tool_to_dict(server_name: ServerName, tool: Tool) -> dict[str, Any]:
    return {
        "server_name": server_name,
        **tool.model_dump(mode="json", by_alias=True, exclude_none=True),
    }
