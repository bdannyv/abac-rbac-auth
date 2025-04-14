from unittest.mock import patch

import pytest_asyncio
from core.data_storage import DB_URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


@pytest_asyncio.fixture(scope="function", autouse=True)
async def mock_session_maker(db_session):
    with patch("auth.core.data_storage.session_maker", new=db_session):
        yield


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
            except Exception as e:
                await trans.rollback()
                raise e
            finally:
                await session.close()
        # Rollback the outer transaction regardless of what happened inside the test
    await engine.dispose()
