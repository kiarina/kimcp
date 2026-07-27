import httpx

from kimcp.core.mcp_server import mcp_server_registry


async def test_list_mcp_servers_returns_connected_servers(
    client: httpx.AsyncClient,
    math_mcp_server,
) -> None:
    connect_response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )
    assert connect_response.status_code == 200

    response = await client.get("/agents/test-agent/mcp-servers")

    assert response.status_code == 200

    data = response.json()

    assert data["agent_id"] == "test-agent"
    assert len(data["mcp_servers"]) == 1
    assert data["mcp_servers"][0]["server_name"] == "math"
    assert data["mcp_servers"][0]["connection"]["transport"] == "stdio"
    assert mcp_server_registry.get(agent_id="test-agent", server_name="math") is not None


async def test_list_mcp_servers_returns_empty_list_for_unknown_agent(
    client: httpx.AsyncClient,
) -> None:
    response = await client.get("/agents/unknown-agent/mcp-servers")

    assert response.status_code == 200
    assert response.json() == {
        "agent_id": "unknown-agent",
        "mcp_servers": [],
    }
