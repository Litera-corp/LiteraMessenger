import logging

from pydantic import HttpUrl, Field, ValidationError, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class AppSettings(ConfigBase):
    url: HttpUrl
    host: IPvAnyAddress
    port: int
    env: str
    auth_token: str
    timezone: str
    version: str
    tg_service: str

    model_config = SettingsConfigDict(env_prefix='APP_')


class Config(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)

    @classmethod
    def load(cls) -> "Config":
        instance = cls()

        return instance


try:
    config = Config.load()
except ValidationError as e:
    logging.error(e)