import httpx


async def test_run_tool_executes_tool(
    client: httpx.AsyncClient,
    math_mcp_server,
) -> None:
    connect_response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )
    assert connect_response.status_code == 200

    response = await client.post(
        "/agents/test-agent/mcp-servers/math/tools/add/run",
        json={"args": {"a": 2, "b": 3}},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == "test-agent"
    assert data["server_name"] == "math"
    assert data["tool_name"] == "add"
    assert data["result"] == [
        {
            "id": data["result"][0]["id"],
            "text": "5",
            "type": "text",
        }
    ]


async def test_run_tool_returns_404_for_unknown_tool(
    client: httpx.AsyncClient,
    math_mcp_server,
) -> None:
    connect_response = await client.post(
        "/agents/test-agent/mcp-servers",
        json=math_mcp_server,
    )
    assert connect_response.status_code == 200

    response = await client.post(
        "/agents/test-agent/mcp-servers/math/tools/unknown/run",
        json={"args": {}},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tool not found."
