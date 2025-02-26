from datetime import datetime

from features.authentication.jwt_service import JWTToken
from infra.cache_storage import RedisSingletonClient
from utils.singleton import ParametrizedSingleton


class JwtTokenRepository(ParametrizedSingleton):
    redis = RedisSingletonClient()

    @classmethod
    async def is_token_revoked(cls, token: JWTToken) -> bool:
        revoked = await cls.redis.hgetall(token.jti.urn)
        return revoked is not None

    @classmethod
    async def revoke_token(cls, token: str, exp: int):
        await cls.redis.set(name=token, value=exp, ex=datetime.fromtimestamp(exp) - datetime.now())
