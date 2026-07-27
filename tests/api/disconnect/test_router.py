import httpx

from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import mcp_server_registry


async def test_disconnect_removes_server_and_session(
    client: httpx.AsyncClient,
    math_mcp_server,
) -> None:
    connect_response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )
    assert connect_response.status_code == 200

    response = await client.delete("/agents/test-agent/mcp-servers/math")

    assert response.status_code == 200
    assert response.json() == {
        "agent_id": "test-agent",
        "server_name": "math",
        "disconnected": True,
    }
    assert mcp_server_registry.get(agent_id="test-agent", server_name="math") is None
    assert mcp_client_registry.ensure("test-agent").sessions.get("math") is None


async def test_disconnect_returns_404_for_unknown_server(
    client: httpx.AsyncClient,
) -> None:
    response = await client.delete("/agents/test-agent/mcp-servers/unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Connection not found."
