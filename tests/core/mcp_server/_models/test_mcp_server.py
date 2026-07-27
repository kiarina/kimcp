from kimcp.core.mcp_server import MCPServer, StreamableHTTPConnection


def test_mcp_server_to_lc_connections() -> None:
    server = MCPServer(
        server_name="math",
        connection=StreamableHTTPConnection(
            url="https://example.com/mcp",
            headers={"X-Test": "1"},
            terminate_on_close=True,
        ),
    )

    assert server.to_lc_connections() == {
        "math": {
            "transport": "streamable_http",
            "session_kwargs": {},
            "url": "https://example.com/mcp",
            "headers": {"X-Test": "1"},
            "terminate_on_close": True,
        }
    }
