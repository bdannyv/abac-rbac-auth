import typing
import uuid

import sqlalchemy as sa
from models import DomainEvent
from sqlalchemy import Select


def select_events_of_aggregate(
    aggregate_id: uuid.UUID, aggregate_type: typing.Optional[str] = None, version_offset: typing.Optional[int] = None
) -> sa.Select[tuple[DomainEvent]]:
    q = sa.select(DomainEvent).where(DomainEvent.aggregate_id == aggregate_id).order_by(DomainEvent.aggregate_version)

    if version_offset:
        q = q.where(DomainEvent.aggregate_version >= version_offset)

    if aggregate_type:
        q = q.where(DomainEvent.aggregate_type == aggregate_type)

    return q


def aggregate_exists(aggregate_id: uuid.UUID) -> Select[tuple[bool]]:
    return sa.select(sa.exists().where(DomainEvent.aggregate_id == aggregate_id))
