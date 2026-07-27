import logging
from typing import Any

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from kimcp.core.app import AgentID
from kimcp.core.mcp_server import MCPServer, ServerName

from .._schemas.mcp_session import MCPSession

logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self, agent_id: AgentID) -> None:
        self.agent_id = agent_id
        self.sessions: dict[ServerName, MCPSession] = {}
        self.tools: dict[tuple[ServerName, str], BaseTool] = {}

    async def connect(self, server: MCPServer) -> None:
        server_name = server.server_name
        if server_name in self.sessions:
            return

        client = MultiServerMCPClient(server.to_lc_connections())
        context_manager = client.session(server_name)
        session = await context_manager.__aenter__()
        self.sessions[server_name] = MCPSession(
            server=server,
            context_manager=context_manager,
            session=session,
        )

    async def disconnect(self, server_name: ServerName) -> None:
        session = self.sessions.get(server_name)
        if session is None:
            return

        try:
            await session.context_manager.__aexit__(None, None, None)
            logger.info("MCP session closed: %s", server_name)
        except Exception as exc:
            logger.warning("Failed to close session %s: %s", server_name, exc)
        finally:
            self.sessions.pop(server_name, None)
            self.tools = {
                tool_key: tool
                for tool_key, tool in self.tools.items()
                if tool_key[0] != server_name
            }

    async def disconnect_all(self) -> None:
        for server_name in list(self.sessions):
            await self.disconnect(server_name)

        self.tools.clear()

    async def list_tools(
        self,
        server_names: list[ServerName] | None = None,
    ) -> list[BaseTool]:
        tools: list[BaseTool] = []

        target_server_names = server_names or list(self.sessions.keys())

        for server_name in target_server_names:
            session = self.sessions.get(server_name)
            if session is None:
                raise ValueError(f"MCP server is not connected: {server_name}")

            loaded_tools = await load_mcp_tools(session.session)

            for tool in loaded_tools:
                normalized_tool = _normalize_tool(tool)
                normalized_tool.metadata = {
                    **(normalized_tool.metadata or {}),
                    "server_name": server_name,
                }
                tools.append(normalized_tool)

        self.tools = {
            (tool.metadata["server_name"], tool.name): tool
            for tool in tools
            if tool.metadata and "server_name" in tool.metadata
        }

        return tools

    async def get_tool(
        self,
        server_name: ServerName,
        tool_name: str,
    ) -> BaseTool | None:
        if tool := self.tools.get((server_name, tool_name)):
            return tool

        if server_name not in self.sessions:
            raise ValueError(f"MCP server is not connected: {server_name}")

        await self.list_tools([server_name])
        return self.tools.get((server_name, tool_name))


def _normalize_tool(tool: BaseTool) -> BaseTool:
    if isinstance(tool.args_schema, dict):
        tool.args_schema = _normalize_additional_properties(tool.args_schema)

    return tool


def _normalize_additional_properties(schema: Any) -> Any:
    if isinstance(schema, dict):
        new_schema: dict[str, Any] = {}

        for key, value in schema.items():
            if key == "additionalProperties" and not isinstance(value, bool):
                new_schema[key] = False
            elif isinstance(value, dict):
                new_schema[key] = _normalize_additional_properties(value)
            elif isinstance(value, list):
                new_schema[key] = [_normalize_additional_properties(item) for item in value]
            else:
                new_schema[key] = value

        return new_schema

    if isinstance(schema, list):
        return [_normalize_additional_properties(item) for item in schema]

    return schema
