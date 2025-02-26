import datetime

import pytest
import pytest_asyncio
from features.authentication.repos.jwt_token import JwtTokenRepository
from infra.cache_storage import CacheStorageFactory


@pytest_asyncio.fixture(scope="function")
async def token_repo():
    yield JwtTokenRepository
    # update cache instance to avoid "Event loop is closed" error
    JwtTokenRepository.cache = CacheStorageFactory.get_new_cache_client()


@pytest.mark.asyncio
async def test_token_hasnt_been_revoked(encoded_token, token_repo):
    encoded_token, _ = encoded_token
    revoked = await token_repo.is_token_revoked(encoded_token)
    assert revoked is False


@pytest.mark.asyncio
async def test_token_revoking(encoded_token, token_repo):
    encoded_token, _ = encoded_token
    expires = int((datetime.datetime.now() + datetime.timedelta(minutes=1)).timestamp())
    init_revoked = await token_repo.is_token_revoked(encoded_token)
    await token_repo.revoke_token(encoded_token, exp=expires)
    final_revoked = await token_repo.is_token_revoked(encoded_token)

    assert init_revoked is False
    assert final_revoked is True
