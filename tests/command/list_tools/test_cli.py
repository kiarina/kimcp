import json
import sys
from pathlib import Path

from click.testing import CliRunner

from kimcp.command.connect.stdio import connect_stdio
from kimcp.command.list_tools import list_tools


def test_list_tools_calls_gateway(
    gateway_base_url: str,
    agent_id: str,
    math_mcp_server_path: Path,
) -> None:
    runner = CliRunner()

    connect_result = runner.invoke(
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
    assert connect_result.exit_code == 0

    result = runner.invoke(
        list_tools,
        [
            "--gateway-base-url",
            gateway_base_url,
            "--agent-id",
            agent_id,
            "--server-name",
            "math",
        ],
    )

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["agent_id"] == agent_id
    assert [tool["name"] for tool in data["tools"]] == ["add", "multiply"]
    assert all(tool["server_name"] == "math" for tool in data["tools"])
