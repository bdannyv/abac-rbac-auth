import typing

import sqlalchemy as sa
from domain.base.event_handler import EventHandlerGroup
from domain.user.event import UserCreatedEvent
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class OnUserCreatedEventHandlerGroup(EventHandlerGroup[UserCreatedEvent]):
    @staticmethod
    async def create_user_projection(event: UserCreatedEvent, session: AsyncSession):
        stmt = sa.insert(User).values(
            {
                User.id: event.aggregate_id,
                User.first_name: event.event_data.first_name,
                User.last_name: event.event_data.last_name,
                User.email: event.event_data.email,
                User.password: event.event_data.password,
            }
        )
        await session.execute(stmt)

    handlers: list[typing.Callable[[UserCreatedEvent], typing.Any]] = [create_user_projection]
