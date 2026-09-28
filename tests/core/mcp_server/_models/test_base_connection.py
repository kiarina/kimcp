from contextlib import AsyncExitStack

from mcp.client.stdio import StdioServerParameters

from kimcp.core.mcp_server import SSEConnection, StdioConnection, StreamableHTTPConnection


async def test_stdio_connection_builds_server_parameters() -> None:
    connection = StdioConnection(
        command="uvx",
        args=["mcp-server"],
        env={"TOKEN": "x"},
        cwd="/tmp",
        encoding="latin-1",
    )

    async with AsyncExitStack() as stack:
        target = await connection.enter_client_target(stack)

    assert isinstance(target, StdioServerParameters)
    assert target.command == "uvx"
    assert target.args == ["mcp-server"]
    assert target.env == {"TOKEN": "x"}
    assert target.cwd == "/tmp"
    assert target.encoding == "latin-1"


async def test_stdio_connection_defaults() -> None:
    async with AsyncExitStack() as stack:
        target = await StdioConnection(command="uvx").enter_client_target(stack)

    assert isinstance(target, StdioServerParameters)
    assert target.env is None
    assert target.encoding == "utf-8"


async def test_http_connections_build_transports() -> None:
    sse = SSEConnection(url="http://example.com/sse", timeout=10, sse_read_timeout=20)
    http = StreamableHTTPConnection(
        url="http://example.com/mcp",
        headers={"X-Test": "1"},
        timeout=10,
        sse_read_timeout=20,
        terminate_on_close=False,
    )

    async with AsyncExitStack() as stack:
        # Transports are async context managers; building them opens no connection.
        assert hasattr(await sse.enter_client_target(stack), "__aenter__")
        assert hasattr(await http.enter_client_target(stack), "__aenter__")
