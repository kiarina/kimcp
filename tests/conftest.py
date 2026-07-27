from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
async def clear_state():
    from kimcp.core.mcp_client import mcp_client_registry
    from kimcp.core.mcp_gateway import mcp_gateway_process_info_store
    from kimcp.core.mcp_server import mcp_server_registry

    yield
    await mcp_client_registry.close_all()
    mcp_gateway_process_info_store.clear()
    mcp_server_registry.clear()


@pytest.fixture(autouse=True)
def setup_app_settings(tmp_path):
    from kimcp.core.app import settings_manager

    settings_manager.cli_args = {
        "user_data_dir": str(tmp_path / "user_data"),
    }
    yield
    settings_manager.cli_args = {}


@pytest.fixture
def math_mcp_server_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "mcp_server_impl" / "math.py"
