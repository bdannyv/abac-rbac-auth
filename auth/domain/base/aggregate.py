import dataclasses
import datetime
import typing
import uuid

from domain.base.exc import AggregateHasNoEventHandler


class EventProtocol(typing.Protocol):
    def get_type(self) -> type["EventProtocol"]:
        pass


EventType = typing.TypeVar("EventType", bound=EventProtocol)
AggregateType = typing.TypeVar("AggregateType")
AggregateEventHandler = typing.Callable[[AggregateType, EventType], AggregateType]


@dataclasses.dataclass
class Aggregate:
    id: uuid.UUID
    version: int
    changes: list[EventType]
    application_map: typing.Mapping[type[EventType], AggregateEventHandler]
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    async def apply(self, event: EventType) -> typing.Self:
        handler = self.application_map.get(event.get_type())
        if handler is None:
            raise AggregateHasNoEventHandler(self, event)

        return await handler(self, event)

    async def load_from_history(self, events: typing.Iterable[EventType]):
        for event in events:
            await self.apply(event)

        return self
