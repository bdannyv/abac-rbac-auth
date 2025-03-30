import datetime
import uuid

import factory
import pytest
import pytest_asyncio
from core.data_storage import DB_URL
from factory import Factory
from features.authentication.api.v1.schemas import SignUpFormModel
from features.authentication.jwt_service import JWTService, JWTToken
from settings.auth import auth_settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from tests.auth.model_factories.models import UserFactory


@pytest.fixture
def token():
    return JWTTokenFactory()


@pytest.fixture
def encoded_token(token):
    return JWTService.encode(exp=int(datetime.timedelta(hours=1).total_seconds()))


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine: AsyncEngine = create_async_engine(url=DB_URL)
    async with engine.connect() as conn:
        # Start an outer transaction
        trans = await conn.begin()
        # Begin a nested transaction (SAVEPOINT) for test isolation
        async with conn.begin_nested():
            session = AsyncSession(bind=conn, expire_on_commit=False)
            try:
                yield session
            finally:
                await session.close()
        # Rollback the outer transaction regardless of what happened inside the test
        await trans.rollback()
    await engine.dispose()


class JWTTokenFactory(Factory):
    class Meta:
        model = JWTToken

    ent_id = factory.LazyFunction(uuid.uuid4)
    jti = factory.LazyFunction(uuid.uuid4)
    iss = "test session"
    aud = auth_settings.jwt_aud
    exp = factory.LazyFunction(lambda: int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()))


class UserCreateFactory(Factory):
    class Meta:
        model = SignUpFormModel

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


@pytest_asyncio.fixture
async def user_create_form():
    return UserCreateFactory()


@pytest_asyncio.fixture
async def user_record():
    return UserFactory()


@pytest_asyncio.fixture(autouse=True)
def register_factories(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
