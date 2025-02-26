import functools
import typing

from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSetting(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")

    host_name: str
    port: int
    db: int
    password: typing.Optional[str] = None
    scheme: str


@functools.cache
def get_redis_settings() -> RedisSetting:
    return RedisSetting()
