import httpx


async def test_list_tools_returns_server_tools(
    client: httpx.AsyncClient,
    math_mcp_server,
) -> None:
    connect_response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )
    assert connect_response.status_code == 200

    response = await client.get("/agents/test-agent/mcp-servers/math/tools")

    assert response.status_code == 200

    data = response.json()

    assert data["agent_id"] == "test-agent"
    assert [tool["name"] for tool in data["tools"]] == ["add", "multiply"]
    assert all(tool["server_name"] == "math" for tool in data["tools"])


async def test_list_tools_returns_404_for_unknown_server(
    client: httpx.AsyncClient,
) -> None:
    response = await client.get("/agents/test-agent/mcp-servers/unknown/tools")

    assert response.status_code == 404
    assert response.json()["detail"] == "MCP Server not found."
