import os
import shutil
import subprocess
from pathlib import Path

import pytest

from .._helpers import (
    find_free_port,
    terminate_process,
    wait_for_http_ready,
)


@pytest.fixture
def setup_gateway_process() -> None:
    # Overridden by command/conftest.py to avoid starting the gateway process twice.
    pass


def test_serve_starts_gateway(tmp_path: Path) -> None:
    host = "127.0.0.1"
    port = find_free_port()
    base_url = f"http://{host}:{port}"
    env = os.environ.copy()
    env["KIMCP_APP_USER_DATA_DIR"] = str(tmp_path)

    uv = shutil.which("uv") or "uv"

    process = subprocess.Popen(
        [
            uv,
            "run",
            "kimcp",
            "serve",
            "--host",
            host,
            "--port",
            str(port),
            "--no-reload",
        ],
        cwd=str(Path(__file__).resolve().parents[3]),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    try:
        wait_for_http_ready(base_url)
        assert process.poll() is None
        assert (tmp_path / "servers" / f"{host}_{port}.json").exists()
    finally:
        terminate_process(process)
