import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSetting(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")

    host_name: str
    port: int
    db: int


@functools.cache
def get_redis_settings() -> RedisSetting:
    return RedisSetting()
