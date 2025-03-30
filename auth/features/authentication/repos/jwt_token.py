from datetime import datetime

from core.cache_storage import CacheStorage, CacheStorageFactory
from utils.singleton import ParametrizedSingleton


class JwtTokenRepository(ParametrizedSingleton):
    cache: CacheStorage = CacheStorageFactory.get_cache_client()

    @classmethod
    async def is_token_revoked(cls, token: str) -> bool:
        revoked = await cls.cache.exists(token)
        return bool(revoked)

    @classmethod
    async def revoke_token(cls, token: str, exp: int):
        await cls.cache.set(name=token, value=exp, ex=datetime.fromtimestamp(exp) - datetime.now())
