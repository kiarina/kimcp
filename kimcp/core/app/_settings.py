from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings_manager import SettingsManager


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="KIMCP_APP_",
        extra="ignore",
    )

    user_data_dir: str | None = None


settings_manager = SettingsManager(AppSettings)
