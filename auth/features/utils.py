from core.cache_storage import CacheStorageFactory
from fastapi import HTTPException, Request, status
from utils.singleton import Singleton

REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
ACCESS_TOKEN_COOKIE_NAME = "access_token"


class AccessTokenDependency(Singleton):
    redis_client = CacheStorageFactory.get_cache_client()

    async def __call__(self, request: Request) -> str:
        token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        revoked = await self.redis_client.exists(token)
        if revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return token


access_token_cookie = AccessTokenDependency()
