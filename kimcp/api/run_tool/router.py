from typing import Any

from fastapi import APIRouter, HTTPException

from kimcp.api.run_tool.request import RunToolRequest
from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import mcp_server_registry

router = APIRouter()


@router.post("/agents/{agent_id}/mcp-servers/{server_name}/tools/{tool_name}/run")
async def run_tool(
    agent_id: AgentID,
    server_name: str,
    tool_name: str,
    request: RunToolRequest,
) -> dict[str, Any]:
    server = mcp_server_registry.get(agent_id=agent_id, server_name=server_name)
    if server is None:
        raise HTTPException(status_code=404, detail="MCP Server not found.")

    client = mcp_client_registry.ensure(agent_id=agent_id)
    try:
        tool = await client.get_tool(server_name, tool_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found.")

    try:
        result = await tool.ainvoke(request.args)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "agent_id": agent_id,
        "server_name": server_name,
        "tool_name": tool_name,
        "result": result,
    }
