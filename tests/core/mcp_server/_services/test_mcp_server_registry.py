from kimcp.core.mcp_server import MCPServer, StdioConnection, mcp_server_registry


def test_register_get_and_list_are_scoped_by_agent() -> None:
    server = MCPServer(
        server_name="math",
        connection=StdioConnection(command="python"),
    )

    mcp_server_registry.register(agent_id="agent-a", server=server)

    assert mcp_server_registry.get(agent_id="agent-a", server_name="math") == server
    assert mcp_server_registry.get(agent_id="agent-b", server_name="math") is None
    assert mcp_server_registry.list(agent_id="agent-a") == [server]
    assert mcp_server_registry.list(agent_id="agent-b") == []


def test_delete_removes_only_target_server() -> None:
    math_server = MCPServer(
        server_name="math",
        connection=StdioConnection(command="python"),
    )
    search_server = MCPServer(
        server_name="search",
        connection=StdioConnection(command="python"),
    )

    mcp_server_registry.register(agent_id="agent-a", server=math_server)
    mcp_server_registry.register(agent_id="agent-a", server=search_server)

    mcp_server_registry.delete(agent_id="agent-a", server_name="math")

    assert mcp_server_registry.get(agent_id="agent-a", server_name="math") is None
    assert mcp_server_registry.get(agent_id="agent-a", server_name="search") == search_server
    assert mcp_server_registry.list(agent_id="agent-a") == [search_server]


def test_clear_removes_all_registered_servers() -> None:
    mcp_server_registry.register(
        agent_id="agent-a",
        server=MCPServer(
            server_name="math",
            connection=StdioConnection(command="python"),
        ),
    )

    mcp_server_registry.clear()

    assert mcp_server_registry.list(agent_id="agent-a") == []
