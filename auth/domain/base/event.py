import abc
import dataclasses
import datetime
import typing
import uuid


class EventBase(abc.ABC):
    def get_type(self):
        return self.__class__


@dataclasses.dataclass
class EventCausation:
    causation_type: type[EventBase]
    causation_id: typing.Any


@dataclasses.dataclass
class Event(EventBase):
    id: uuid.UUID
    event_type: type[EventBase]
    event_version: int
    event_data: dict

    aggregate_id: uuid.UUID
    aggregate_type: str

    correlation_id: uuid.UUID
    causation: EventCausation

    timestamp: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
