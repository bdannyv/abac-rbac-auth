import functools
import typing

from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")

    host_name: str
    port: typing.Optional[int] = None
    user: str
    password: str
    db: str
    default_schema: typing.Optional[str] = "public"


@functools.cache
def get_storage_settings() -> PostgresSettings:
    return PostgresSettings()
