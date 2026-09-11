import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Zombie Run Cost Killer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "trainpilot"
    POSTGRES_PASSWORD: str = "trainpilot_secret_pass"
    POSTGRES_DB: str = "trainpilot_db"
    POSTGRES_PORT: str = "5432"
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Defaults
    STORAGE_BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage"))
    DEFAULT_OUTPUT_FOLDER: str = "./storage/outputs"
    DEFAULT_CHECKPOINT_FOLDER: str = "./storage/checkpoints"
    THEME: str = "dark"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
