import asyncio
import logging
import os
import sys
from pathlib import Path

import pytest

from kimcp.core.mcp_client import MCPClient
from kimcp.core.mcp_server import MCPServer, StdioConnection


def _math_server(math_mcp_server_path: Path) -> MCPServer:
    return MCPServer(
        server_name="math",
        connection=StdioConnection(
            command=sys.executable,
            args=[str(math_mcp_server_path)],
        ),
    )


def _is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False

    return True


async def test_mcp_client_happy_path(math_mcp_server_path: Path) -> None:
    client = MCPClient(agent_id="test-agent")
    server = _math_server(math_mcp_server_path)

    await client.connect(server)

    assert client.sessions["math"].server == server

    tools = await client.list_tools()

    assert [(server_name, tool.name) for server_name, tool in tools] == [
        ("math", "add"),
        ("math", "multiply"),
        ("math", "pid"),
        ("math", "fail"),
    ]

    tool = await client.get_tool("math", "add")

    assert tool is not None
    assert tool.name == "add"

    result = await client.call_tool("math", "add", {"a": 1, "b": 2})

    assert result.structured_content == {"result": 3}
    assert result.is_error is False

    await client.disconnect("math")

    assert client.sessions == {}
    assert client.tools == {}

    await client.disconnect_all()

    assert client.sessions == {}
    assert client.tools == {}


async def test_mcp_client_works_across_tasks(
    math_mcp_server_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    # The gateway connects, calls and disconnects from separate request tasks.
    client = MCPClient(agent_id="test-agent")

    await asyncio.create_task(client.connect(_math_server(math_mcp_server_path)))
    result = await asyncio.create_task(client.call_tool("math", "pid", {}))
    assert result.structured_content is not None
    pid = result.structured_content["result"]
    assert _is_running(pid)

    with caplog.at_level(logging.WARNING):
        await asyncio.create_task(client.disconnect("math"))

    assert "Failed to close session" not in caplog.text
    for _ in range(50):
        if not _is_running(pid):
            break
        await asyncio.sleep(0.1)
    assert not _is_running(pid)


async def test_mcp_client_raises_for_unknown_server() -> None:
    client = MCPClient(agent_id="test-agent")

    with pytest.raises(ValueError, match="MCP server is not connected: missing"):
        await client.list_tools(["missing"])

    with pytest.raises(ValueError, match="MCP server is not connected: missing"):
        await client.call_tool("missing", "add", {})
