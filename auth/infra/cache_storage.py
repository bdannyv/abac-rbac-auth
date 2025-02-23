from redis.asyncio import Redis
from utils.singleton import ParametrizedSingleton, ParametrizedSingletonMeta


class RedisParametrizedSingletonMeta(ParametrizedSingletonMeta, type(Redis)):
    # metaclass conflict resolver
    ...


class RedisSingletonClient(ParametrizedSingleton, Redis, metaclass=RedisParametrizedSingletonMeta):
    ...
