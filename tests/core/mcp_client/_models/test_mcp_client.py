import sys
from pathlib import Path

from kimcp.core.mcp_client import MCPClient
from kimcp.core.mcp_server import MCPServer, StdioConnection


async def test_mcp_client_happy_path(math_mcp_server_path: Path) -> None:
    client = MCPClient(agent_id="test-agent")
    server = MCPServer(
        server_name="math",
        connection=StdioConnection(
            command=sys.executable,
            args=[str(math_mcp_server_path)],
        ),
    )

    await client.connect(server)

    assert client.sessions["math"].server == server

    tools = await client.list_tools()

    assert [tool.name for tool in tools] == ["add", "multiply"]

    tool = await client.get_tool("math", "add")

    assert tool is not None
    assert tool.name == "add"
    assert tool.metadata is not None
    assert tool.metadata["server_name"] == "math"

    await client.disconnect("math")

    assert client.sessions == {}
    assert client.tools == {}

    await client.disconnect_all()

    assert client.sessions == {}
    assert client.tools == {}
