import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import httpx
import pytest


@pytest.fixture
def math_mcp_server(math_mcp_server_path: Path) -> dict:
    return {
        "server_name": "math",
        "connection": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(math_mcp_server_path)],
        },
    }


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    from kimcp.api.app import app

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        yield client
