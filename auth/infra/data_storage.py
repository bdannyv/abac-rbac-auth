import contextlib

from settings.base import app_settings
from sqlalchemy import URL, orm
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

DB_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=app_settings.storage.user,
    password=app_settings.storage.password,
    host=app_settings.storage.host_name,
    port=app_settings.storage.port,
    database=app_settings.storage.db,
)


class Base(orm.DeclarativeBase):
    """Base declarative class for all DB models"""


engine: AsyncEngine = create_async_engine(url=DB_URL)
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


@contextlib.asynccontextmanager
async def get_session():
    session = session_maker()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    else:
        await session.commit()
    finally:
        await session.close()
