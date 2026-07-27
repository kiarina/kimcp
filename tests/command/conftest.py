import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from ._helpers import (
    find_free_port,
    terminate_process,
    wait_for_http_ready,
)


@pytest.fixture(scope="session")
def gateway_host() -> str:
    return "127.0.0.1"


@pytest.fixture(scope="session")
def gateway_port() -> int:
    return find_free_port()


@pytest.fixture(scope="session")
def gateway_base_url(gateway_host: str, gateway_port: int) -> str:
    return f"http://{gateway_host}:{gateway_port}"


@pytest.fixture(scope="session", autouse=True)
def setup_gateway_process(
    tmp_path_factory: pytest.TempPathFactory,
    gateway_host: str,
    gateway_port: int,
    gateway_base_url: str,
):
    tmp_path = tmp_path_factory.getbasetemp()

    env = os.environ.copy()
    env["KIMCP_APP_USER_DATA_DIR"] = str(tmp_path / "gateway_user_data")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "kimcp.api.app:app",
            "--host",
            gateway_host,
            "--port",
            str(gateway_port),
        ],
        cwd=str(Path(__file__).resolve().parents[1]),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    try:
        wait_for_http_ready(gateway_base_url)
        yield

    finally:
        terminate_process(process)


@pytest.fixture
def agent_id(request: pytest.FixtureRequest) -> str:
    slug = request.node.name.replace("[", "_").replace("]", "_").replace("/", "_")
    return f"{slug}_{uuid.uuid4().hex[:8]}"
