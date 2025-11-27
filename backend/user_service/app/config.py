# app/config.py
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Пример настроек, добавить/удалить поля по необходимости
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_TEST: Optional[str] = None
    SECRET_KEY: str = "change-me-for-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
