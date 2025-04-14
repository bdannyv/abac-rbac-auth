import typing
import uuid

import sqlalchemy as sa
from domain.base.event import DomainEvent
from domain.base.queries import select_events_of_aggregate
from models.domain_event import DomainEvent as DomainEventDBModel
from sqlalchemy.ext.asyncio import AsyncSession


class EventStore:
    @classmethod
    async def get_by_aggregate(cls, session: AsyncSession, aggregate_id: uuid.UUID):
        query = select_events_of_aggregate(aggregate_id=aggregate_id)
        aggregate_events = await session.execute(query)
        return aggregate_events.scalars()

    @classmethod
    async def save(cls, session: AsyncSession, events: typing.Iterable[DomainEvent]):
        if events:
            stmt = sa.insert(DomainEventDBModel).values([event.db_model_dict() for event in events])
            await session.execute(stmt)
