from kimcp.core.mcp_client import MCPClient, mcp_client_registry


async def test_ensure_returns_same_client_for_same_agent() -> None:
    client1 = mcp_client_registry.ensure("agent-a")
    client2 = mcp_client_registry.ensure("agent-a")
    client3 = mcp_client_registry.ensure("agent-b")

    assert client1 is client2
    assert client1 is not client3
    assert isinstance(client1, MCPClient)


async def test_close_all_disconnects_clients_and_clears_registry(monkeypatch) -> None:
    disconnected_agent_ids: list[str] = []

    async def fake_disconnect_all(self: MCPClient) -> None:
        disconnected_agent_ids.append(self.agent_id)

    monkeypatch.setattr(MCPClient, "disconnect_all", fake_disconnect_all)

    client1 = mcp_client_registry.ensure("agent-a")
    client2 = mcp_client_registry.ensure("agent-b")

    await mcp_client_registry.close_all()

    assert sorted(disconnected_agent_ids) == ["agent-a", "agent-b"]
    assert mcp_client_registry.ensure("agent-a") is not client1
    assert mcp_client_registry.ensure("agent-b") is not client2
