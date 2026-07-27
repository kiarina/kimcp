import json
import sys
from pathlib import Path

from click.testing import CliRunner

from kimcp.command.connect.stdio import connect_stdio
from kimcp.command.disconnect import disconnect


def test_disconnect_calls_gateway(
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
        disconnect,
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
    assert json.loads(result.output) == {
        "agent_id": agent_id,
        "disconnected": True,
        "server_name": "math",
    }
