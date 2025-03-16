import typing
import uuid

import sqlalchemy as sa
from features.authentication.models.user import User
from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.dml import ReturningDelete, ReturningInsert, ReturningUpdate


class UserCreateDBInput(typing.TypedDict):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    password: str


def insert_user_query(*user_data: UserCreateDBInput) -> ReturningInsert[tuple[uuid.UUID]]:
    return sa.insert(User).values(*user_data).returning(User.id)


def update_user_query(
    id_: uuid.UUID, to_update: dict[str | InstrumentedAttribute, typing.Any]
) -> ReturningUpdate[tuple[uuid.UUID | None]]:
    return sa.update(User).where(User.id == id_).values(**to_update).returning(User.id)


def delete_user_query(id_: uuid.UUID) -> ReturningDelete[tuple[uuid.UUID | None]]:
    return sa.delete(User).where(User.id == id_).returning(User.id)


def get_user_by_email(email: str) -> Select[tuple[User]]:
    return sa.select(User).where(User.email == email)
