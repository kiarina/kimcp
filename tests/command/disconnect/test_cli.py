import json
import os
import sys
import time
from pathlib import Path

from click.testing import CliRunner

from kimcp.command.connect.stdio import connect_stdio
from kimcp.command.disconnect import disconnect
from kimcp.command.run_tool import run_tool


def _is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False

    return True


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

    pid_result = runner.invoke(
        run_tool,
        [
            "--gateway-base-url",
            gateway_base_url,
            "--agent-id",
            agent_id,
            "--server-name",
            "math",
            "--tool-name",
            "pid",
        ],
    )
    assert pid_result.exit_code == 0
    server_pid = json.loads(pid_result.output)["result"]["structuredContent"]["result"]
    assert _is_running(server_pid)

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

    # The gateway handles each request in its own task; the stdio server must still stop.
    deadline = time.monotonic() + 5
    while _is_running(server_pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert not _is_running(server_pid)
