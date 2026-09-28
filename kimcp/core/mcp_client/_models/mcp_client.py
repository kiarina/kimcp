import logging
from typing import Any

from mcp.types import CallToolResult, Tool

from kimcp.core.app import AgentID
from kimcp.core.mcp_server import MCPServer, ServerName

from .._schemas.mcp_session import MCPSession

logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self, agent_id: AgentID) -> None:
        self.agent_id = agent_id
        self.sessions: dict[ServerName, MCPSession] = {}
        self.tools: dict[tuple[ServerName, str], Tool] = {}

    async def connect(self, server: MCPServer) -> None:
        server_name = server.server_name
        if server_name in self.sessions:
            return

        self.sessions[server_name] = await MCPSession.open(server)

    async def disconnect(self, server_name: ServerName) -> None:
        session = self.sessions.pop(server_name, None)
        self.tools = {
            tool_key: tool for tool_key, tool in self.tools.items() if tool_key[0] != server_name
        }
        if session is None:
            return

        try:
            await session.close()
            logger.info("MCP session closed: %s", server_name)
        except Exception as exc:
            logger.warning("Failed to close session %s: %s", server_name, exc)

    async def disconnect_all(self) -> None:
        for server_name in list(self.sessions):
            await self.disconnect(server_name)

        self.tools.clear()

    async def list_tools(
        self,
        server_names: list[ServerName] | None = None,
    ) -> list[tuple[ServerName, Tool]]:
        tools: list[tuple[ServerName, Tool]] = []

        for server_name in server_names or list(self.sessions):
            session = self._get_session(server_name)
            result = await session.client.list_tools()

            self.tools = {
                tool_key: tool
                for tool_key, tool in self.tools.items()
                if tool_key[0] != server_name
            }
            for tool in result.tools:
                self.tools[(server_name, tool.name)] = tool
                tools.append((server_name, tool))

        return tools

    async def get_tool(self, server_name: ServerName, tool_name: str) -> Tool | None:
        if tool := self.tools.get((server_name, tool_name)):
            return tool

        await self.list_tools([server_name])
        return self.tools.get((server_name, tool_name))

    async def call_tool(
        self,
        server_name: ServerName,
        tool_name: str,
        args: dict[str, Any],
    ) -> CallToolResult:
        session = self._get_session(server_name)
        return await session.client.call_tool(tool_name, args)

    def _get_session(self, server_name: ServerName) -> MCPSession:
        session = self.sessions.get(server_name)
        if session is None:
            raise ValueError(f"MCP server is not connected: {server_name}")

        return session
