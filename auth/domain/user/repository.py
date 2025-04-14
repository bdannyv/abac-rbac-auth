import uuid

from domain.base.repository import AggregateRepository
from domain.user.aggregate import UserAggregate
from domain.user.event import user_event_repo
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
