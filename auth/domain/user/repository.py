import itertools
import uuid

from domain.base.repository import AggregateRepository
from domain.user.aggregate import UserAggregate
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(AggregateRepository[UserAggregate]):
    @classmethod
    async def get(cls, aggregate_id: uuid.UUID, session: AsyncSession) -> UserAggregate | None:
        aggregate_events = await cls.event_store.get_by_aggregate(session, aggregate_id)
        init_event = next(aggregate_events, None)

        if init_event is not None:
            user = await UserAggregate.load_from_history(itertools.chain([init_event], aggregate_events))
        else:
            user = None
        return user
