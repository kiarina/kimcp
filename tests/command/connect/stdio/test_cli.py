import json
import sys
from pathlib import Path

import httpx
from click.testing import CliRunner

from kimcp.command.connect.stdio import connect_stdio


def test_connect_stdio_registers_mcp_server(
    gateway_base_url: str,
    agent_id: str,
    math_mcp_server_path: Path,
) -> None:
    result = CliRunner().invoke(
        connect_stdio,
        [
            "--gateway-base-url",
            gateway_base_url,
            "--agent-id",
            agent_id,
            "--server-name",
            "math",
            "--command",
            sys.executable,
            "--arg",
            str(math_mcp_server_path),
        ],
    )

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["agent_id"] == agent_id
    assert data["mcp_server"]["server_name"] == "math"
    assert data["mcp_server"]["connection"]["transport"] == "stdio"
    response = httpx.get(f"{gateway_base_url}/agents/{agent_id}/mcp-servers")
    assert response.status_code == 200
    assert [server["server_name"] for server in response.json()["mcp_servers"]] == ["math"]
