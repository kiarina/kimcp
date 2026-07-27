from platformdirs import user_data_dir

from .._settings import settings_manager


def get_user_data_dir() -> str:
    settings = settings_manager.get_settings()

    if settings.user_data_dir:
        return settings.user_data_dir

    return user_data_dir(appname="kimcp")
