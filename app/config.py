import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    WEBHOOK_SECRET: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/app.db"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
