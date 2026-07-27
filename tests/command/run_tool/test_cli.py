import json
import sys
from pathlib import Path

from click.testing import CliRunner

from kimcp.command.connect.stdio import connect_stdio
from kimcp.command.run_tool import run_tool


def test_run_tool_calls_gateway(
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
        run_tool,
        [
            "--gateway-base-url",
            gateway_base_url,
            "--agent-id",
            agent_id,
            "--server-name",
            "math",
            "--tool-name",
            "add",
            "--tool-args",
            '{"a":1,"b":2}',
        ],
    )

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["agent_id"] == agent_id
    assert data["server_name"] == "math"
    assert data["tool_name"] == "add"
    assert data["result"][0]["text"] == "3"
