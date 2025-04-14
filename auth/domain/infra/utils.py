import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession


async def pg_advisory_lock(value, session: AsyncSession):
    await session.execute(sa.text("SELECT pg_advisory_xact_lock(hashtext(:email))"), {"email": value})
