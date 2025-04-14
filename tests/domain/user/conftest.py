import pytest_asyncio

from tests.table_factories.user import UserFactory


@pytest_asyncio.fixture
async def user_record():
    return UserFactory()


@pytest_asyncio.fixture(autouse=True)
def register_factories(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    yield
