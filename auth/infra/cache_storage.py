from redis.asyncio import Redis
from settings.base import app_settings
from utils.singleton import ParametrizedSingleton, ParametrizedSingletonMeta


class RedisParametrizedSingletonMeta(ParametrizedSingletonMeta, type(Redis)):
    # metaclass conflict resolver
    ...


class RedisSingletonClient(ParametrizedSingleton, Redis, metaclass=RedisParametrizedSingletonMeta):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["host"] = app_settings.cache.host_name
        kwargs["port"] = app_settings.cache.port
        kwargs["db"] = app_settings.cache.db
        kwargs["password"] = app_settings.cache.password
        super().__init__(*args, **kwargs)
