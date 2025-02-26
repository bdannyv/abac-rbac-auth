import abc
import functools

from settings.base import app_settings


class CacheStorage:
    @abc.abstractmethod
    async def exists(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def close(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def hgetall(self, key):
        ...

    @abc.abstractmethod
    async def set(self, name, value, *args, **kwargs):
        ...


class CacheStorageFactory:
    @classmethod
    @functools.cache
    def get_cache_client(cls) -> CacheStorage:
        return cls.get_new_cache_client()

    @classmethod
    def get_new_cache_client(cls) -> CacheStorage:
        from redis.asyncio import Redis

        class RedisCacheClient(Redis, CacheStorage):
            def __init__(self, *args, **kwargs) -> None:
                kwargs["host"] = app_settings.cache.host_name
                kwargs["port"] = app_settings.cache.port
                kwargs["db"] = app_settings.cache.db
                kwargs["password"] = app_settings.cache.password
                super().__init__(*args, **kwargs)

        return RedisCacheClient()
