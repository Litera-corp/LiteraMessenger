# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-for-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
