import pytest

from kimcp.core.mcp_server._models.sse_connection import SSEConnection
from kimcp.core.mcp_server._models.stdio_connection import StdioConnection
from kimcp.core.mcp_server._models.streamable_http_connection import (
    StreamableHTTPConnection,
)


@pytest.mark.parametrize(
    ("connection", "expected"),
    [
        (
            SSEConnection(
                url="http://example.com/sse",
                headers={"Authorization": "Bearer token"},
                timeout=None,
                sse_read_timeout=30.0,
            ),
            {
                "transport": "sse",
                "url": "http://example.com/sse",
                "headers": {"Authorization": "Bearer token"},
                "session_kwargs": {},
                "sse_read_timeout": 30.0,
            },
        ),
        (
            StdioConnection(
                command="uvx",
                args=["mcp-server"],
                cwd=None,
                encoding="utf-8",
            ),
            {
                "transport": "stdio",
                "command": "uvx",
                "args": ["mcp-server"],
                "env": {},
                "session_kwargs": {},
                "encoding": "utf-8",
            },
        ),
        (
            StreamableHTTPConnection(
                url="http://example.com/mcp",
                timeout=10.0,
                sse_read_timeout=None,
                terminate_on_close=True,
            ),
            {
                "transport": "streamable_http",
                "url": "http://example.com/mcp",
                "headers": {},
                "timeout": 10.0,
                "terminate_on_close": True,
                "session_kwargs": {},
            },
        ),
    ],
)
def test_to_connection_returns_transport_specific_payload(connection, expected) -> None:
    assert connection.to_connection() == expected
