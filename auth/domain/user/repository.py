import uuid

from domain.base.repository import AggregateRepository
from domain.user.aggregate import UserAggregate
from domain.user.event import user_event_repo
from domain.user.exc import UserNotFound
from domain.user.queries import get_user_by_login_query
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(AggregateRepository[UserAggregate]):
    @classmethod
    async def get(cls, aggregate_id: uuid.UUID, session: AsyncSession) -> UserAggregate | None:
        aggregate_events = await cls.event_store.get_by_aggregate(session, aggregate_id)
        events = [user_event_repo[event.event_type].model_validate(event) for event in aggregate_events]

        if events:
            user = await UserAggregate.load_from_history(events)
        else:
            user = None
        return user

    @classmethod
    async def get_by_login(cls, login: str, session: AsyncSession) -> UserAggregate:
        query = get_user_by_login_query(login)
        result = await session.execute(query)
        aggregate_id = result.scalar_one_or_none()

        if aggregate_id is None:
            raise UserNotFound()

        user = await cls.get(aggregate_id, session)
        if user is None: # Should not happen if aggregate_id was found, means DB inconsistency or event issue
            raise UserNotFound(f"User with login '{login}' has ID {aggregate_id} but no events were found.")
        return user
