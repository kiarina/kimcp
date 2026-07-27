from typing import Any

from fastapi import APIRouter, HTTPException
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from kimcp.core.app import AgentID
from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import mcp_server_registry

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
        "tools": [_tool_to_dict(tool) for tool in tools],
    }


def _tool_to_dict(tool: BaseTool) -> dict[str, Any]:
    args_schema: dict[str, Any] | None = None

    if isinstance(tool.args_schema, dict):
        args_schema = tool.args_schema
    elif isinstance(tool.args_schema, type) and issubclass(tool.args_schema, BaseModel):
        args_schema = tool.args_schema.model_json_schema()

    return {
        "server_name": tool.metadata.get("server_name") if tool.metadata else None,
        "name": tool.name,
        "description": tool.description,
        "args_schema": args_schema,
    }
