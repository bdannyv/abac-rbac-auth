import functools
import typing

from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="data_storage_")

    host: str
    port: typing.Optional[int] = None
    user: str
    password: str
    database: str
    default_schema: typing.Optional[str] = "public"


@functools.cache
def get_storage_settings():
    return StorageSettings()


storage_settings = get_storage_settings()
