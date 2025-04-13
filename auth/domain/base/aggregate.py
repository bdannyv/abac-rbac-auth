import dataclasses
import datetime
import typing
import uuid

from domain.base.event import DomainEvent
from domain.base.exc import AggregateHasNoEventHandler


class EventProtocol(typing.Protocol):
    def get_type(self) -> type["EventProtocol"]:
        pass


T = typing.TypeVar("T", bound=DomainEvent)


class AggregateEventHandler(typing.Protocol):
    async def __call__(self, event: T) -> None:
        ...


@dataclasses.dataclass
class Aggregate:
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    version: typing.Optional[int] = dataclasses.field(default=0)
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    uncommitted_events: list[DomainEvent] = dataclasses.field(default_factory=list)
    _application_map: dict[type[T], AggregateEventHandler] = dataclasses.field(default_factory=dict)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_events()
        if exc_val:
            raise exc_val

    @classmethod
    def get_type(cls):
        return cls.__name__

    def get_version_increment(self):
        self.version += 1
        return self.version

    def record_event(self, event: DomainEvent):
        self.uncommitted_events.append(event)

    def record_events(self, *events: DomainEvent):
        self.uncommitted_events.extend(events)

    def reset_events(self):
        self.uncommitted_events = []

    async def apply(self, event: DomainEvent) -> typing.Self:
        handler = self._application_map.get(event.get_type())
        if handler is None:
            raise AggregateHasNoEventHandler(self, event)

        await handler(event)

    @classmethod
    async def load_from_history(cls, events: typing.Iterable[DomainEvent]) -> "Aggregate":
        aggregate = cls()

        await cls.hydrate(aggregate, events)

        return aggregate

    async def hydrate(self, events: typing.Iterable[DomainEvent]):
        for event in events:
            await self.apply(event)
