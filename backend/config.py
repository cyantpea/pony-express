"""Application configuration module.

Args:
    settings (Settings): The settings for the application
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Model for application settings.

    Any default settings will be overwritten by environment variables.
    """

    app_title: str
    app_description: str
    db_url: str
    db_sqlite: bool
    jwt_algorithm: str
    jwt_cookie_key: str
    jwt_duration: int
    jwt_issuer: str
    jwt_secret_key: str = "super-secret-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    """Get the application settings."""

    return Settings(
        app_title="pony express",
        app_description="A social messaging app",
        db_url="sqlite:///backend/database/development.db",
        db_sqlite=True,
        jwt_algorithm="HS256",
        jwt_cookie_key="pony-express-token",
        jwt_duration=3600,
        jwt_issuer="http://127.0.0.1",
    )


settings = get_settings()
