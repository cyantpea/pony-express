from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Model for application settings."""

    app_title: str = "pony express"
    app_description: str = "A social messaging app"
    db_url: str = "sqlite:///backend/database/development.db"
    db_sqlite: bool = True
    jwt_algorithm: str = "HS256"
    jwt_cookie_key: str = "pony-express-token"
    jwt_duration: int = 3600
    jwt_issuer: str = "http://127.0.0.1"
    jwt_secret_key: str = "super-secret-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
