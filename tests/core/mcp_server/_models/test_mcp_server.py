from kimcp.core.mcp_server import MCPServer, StreamableHTTPConnection


def test_mcp_server_keeps_the_connection_config() -> None:
    server = MCPServer.model_validate(
        {
            "server_name": "math",
            "connection": {
                "transport": "streamable_http",
                "url": "https://example.com/mcp",
                "headers": {"X-Test": "1"},
                "terminate_on_close": True,
            },
        }
    )

    assert isinstance(server.connection, StreamableHTTPConnection)
    assert server.model_dump(mode="json", exclude_none=True) == {
        "server_name": "math",
        "connection": {
            "transport": "streamable_http",
            "session_kwargs": {},
            "url": "https://example.com/mcp",
            "headers": {"X-Test": "1"},
            "terminate_on_close": True,
        },
    }
