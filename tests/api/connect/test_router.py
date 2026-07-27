import httpx

from kimcp.core.mcp_client import mcp_client_registry
from kimcp.core.mcp_server import mcp_server_registry


async def test_connect(client: httpx.AsyncClient, math_mcp_server) -> None:
    response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["agent_id"] == "test-agent"
    assert data["mcp_server"]["server_name"] == "math"
    assert data["mcp_server"]["connection"]["transport"] == "stdio"

    assert mcp_server_registry.get(agent_id="test-agent", server_name="math") is not None
    assert mcp_client_registry.ensure("test-agent").sessions.get("math") is not None


async def test_invalid_payload(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/agents/test-agent/mcp-servers",
        json={"server_name": "math"},
    )

    assert response.status_code == 422
