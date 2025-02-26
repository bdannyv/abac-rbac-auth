import datetime
import uuid

import factory
import pytest
import pytest_asyncio
from factory import Factory
from features.authentication.jwt_service import JWTService, JWTToken
from infra.data_storage import session_maker
from settings.auth import auth_settings

from tests.auth.model_factories.models import UserFactory


@pytest.fixture
def token():
    return JWTTokenFactory()


@pytest.fixture
def encoded_token(token):
    return JWTService.encode(exp=int(datetime.timedelta(hours=1).total_seconds()))


@pytest_asyncio.fixture
async def db_session():
    session = session_maker()

    async with session.begin() as transaction:
        try:
            yield session
        finally:
            await transaction.rollback()
            await session.close()


class JWTTokenFactory(Factory):
    class Meta:
        model = JWTToken

    ent_id = factory.LazyFunction(uuid.uuid4)
    jti = factory.LazyFunction(uuid.uuid4)
    iss = "test session"
    aud = auth_settings.jwt_aud
    exp = factory.LazyFunction(lambda: int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()))


@pytest_asyncio.fixture(autouse=True)
def register_factories(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
