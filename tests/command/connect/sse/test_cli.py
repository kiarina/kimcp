import json
import os
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path

import httpx
import pytest
from click.testing import CliRunner

from kimcp.command.connect.sse import connect_sse

from ..._helpers import find_free_port, terminate_process, wait_for_socket


@pytest.fixture
def sse_math_mcp_server_url(math_mcp_server_path: Path) -> Generator[str, None, None]:
    host = "127.0.0.1"
    port = find_free_port()
    process = subprocess.Popen(
        [
            sys.executable,
            str(math_mcp_server_path),
            "--transport",
            "sse",
            "--host",
            host,
            "--port",
            str(port),
        ],
        cwd=str(math_mcp_server_path.parent),
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    try:
        wait_for_socket(host, port)
        yield f"http://{host}:{port}/sse"
    finally:
        terminate_process(process)


def test_connect_sse_registers_mcp_server(
    gateway_base_url: str,
    agent_id: str,
    sse_math_mcp_server_url: str,
) -> None:
    result = CliRunner().invoke(
        connect_sse,
        [
            "--gateway-base-url",
            gateway_base_url,
            "--agent-id",
            agent_id,
            "--server-name",
            "math",
            "--url",
            sse_math_mcp_server_url,
            "--timeout",
            "10",
            "--sse-read-timeout",
            "20",
        ],
    )

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["agent_id"] == agent_id
    assert data["mcp_server"]["server_name"] == "math"
    assert data["mcp_server"]["connection"]["transport"] == "sse"
    response = httpx.get(f"{gateway_base_url}/agents/{agent_id}/mcp-servers")
    assert response.status_code == 200
    assert [server["server_name"] for server in response.json()["mcp_servers"]] == ["math"]
