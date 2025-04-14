import abc
import typing
import uuid

from domain.base.queries import aggregate_exists
from domain.infra.event_store import EventStore
from sqlalchemy.ext.asyncio import AsyncSession

AggregateType = typing.TypeVar("AggregateType")


class AggregateRepository(abc.ABC, typing.Generic[AggregateType]):
    event_store: EventStore = EventStore

    @classmethod
    @abc.abstractmethod
    async def get(cls, aggregate_id: uuid.UUID, session: AsyncSession) -> AggregateType:
        pass

    @classmethod
    async def save(cls, aggregate: AggregateType, session: AsyncSession):
        await cls.event_store.save(session, aggregate.uncommitted_events)

    @classmethod
    async def exists(cls, aggregate_id: uuid.UUID, session: AsyncSession):
        exists_res = await session.execute(aggregate_exists(aggregate_id))
        return exists_res.scalar()
