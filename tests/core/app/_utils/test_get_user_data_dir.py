import pytest

from kimcp.core.app import get_user_data_dir, settings_manager


@pytest.fixture(autouse=True)
def setup_app_settings():
    yield
    settings_manager.cli_args = {}


def test_default() -> None:
    assert "kimcp" in get_user_data_dir()


def test_custom_user_data_dir(tmp_path) -> None:
    settings_manager.cli_args = {"user_data_dir": str(tmp_path)}
    assert get_user_data_dir() == str(tmp_path)
