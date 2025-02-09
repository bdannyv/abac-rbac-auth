import typing
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from features.authentication.models.user import User
from features.authentication.queries import delete_user_query, get_user_by_email, insert_user_query, update_user_query


class UserCreate(typing.Protocol):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    password: str


class UserRepository:
    @staticmethod
    async def get(id_: uuid.UUID, session: AsyncSession) -> User | None:
        return await session.get(User, id_)

    @staticmethod
    async def create(user_data: UserCreate, session: AsyncSession) -> uuid.UUID:
        stmt = insert_user_query(
            {
                "id": user_data.id,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "password": user_data.password,
            }
        )

        stmt_res = await session.execute(stmt)
        return stmt_res.scalar()

    @staticmethod
    async def update(
        id_: uuid.UUID, user_data: dict[str | InstrumentedAttribute, typing.Any], session: AsyncSession
    ) -> uuid.UUID | None:
        stmt = update_user_query(id_=id_, to_update=user_data)
        stmt_res = await session.execute(stmt)
        return stmt_res.scalar()

    @staticmethod
    async def delete(id_: uuid.UUID, session: AsyncSession) -> uuid.UUID | None:
        stmt = delete_user_query(id_=id_)
        stmt_res = await session.execute(stmt)
        return stmt_res.scalar()

    @staticmethod
    async def get_by_email(email: str, session: AsyncSession) -> User | None:
        stmt = get_user_by_email(email)
        stmt_res = await session.execute(stmt)
        return stmt_res.scalar()
