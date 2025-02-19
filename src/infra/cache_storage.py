from redis.asyncio import Redis

from utils.singleton import Singleton, SingletonMeta


class RedisSingletonMeta(SingletonMeta, type(Redis)):
    # metaclass conflict resolver
    ...


class RedisSingletonClient(Singleton, Redis, metaclass=RedisSingletonMeta):
    ...
