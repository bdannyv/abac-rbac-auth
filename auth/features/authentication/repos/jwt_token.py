from features.authentication.jwt_service import JWTToken
from infra.cache_storage import RedisSingletonClient
from utils.singleton import Singleton


class JwtTokenRepository(Singleton):
    redis = RedisSingletonClient()

    @classmethod
    async def is_token_revoked(cls, token: JWTToken) -> bool:
        revoked = await cls.redis.hgetall(token.jti.urn)
        return revoked is not None

    @classmethod
    async def revoke_token(cls, token: JWTToken):
        async with cls.redis.pipeline() as pipeline:
            await pipeline.hset(token.jti.urn, token.model_dump_json())
            await pipeline.expire(token.jti.urn, time=token.exp - token.iss)

            await pipeline.execute()
