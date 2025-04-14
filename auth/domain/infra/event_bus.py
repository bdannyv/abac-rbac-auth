import asyncio
import typing

from domain.base.event import DomainEvent
from domain.user.event import UserCreatedEvent
from domain.user.event_handler import OnUserCreatedEventHandlerGroup

DomainEventType = typing.TypeVar("DomainEventType")


class EventHandlerGroupProtocol(typing.Protocol):
    event: DomainEventType
    handlers: list[typing.Callable[[DomainEventType], typing.Any]]

    @classmethod
    async def handle_event(cls, event: DomainEvent):
        pass

    @classmethod
    async def get_type_str(cls):
        pass


class EventBus:
    _event_handler_map_: dict[type[DomainEvent], list[EventHandlerGroupProtocol]] = {
        UserCreatedEvent: [OnUserCreatedEventHandlerGroup]
    }

    @classmethod
    async def publish(cls, *events: DomainEvent):
        for event in events:
            event_handler_groups = cls._event_handler_map_[event.get_type()]

            tasks = [
                asyncio.create_task(
                    handlers.handle_event(event),
                    name=f"Handler: {handlers.get_type_str()}. Event: {event.get_type_str}-{event.id}",
                )
                for handlers in event_handler_groups
            ]

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

            task = next(filter(lambda x: x.exception(), done), None)
            if task is not None:
                raise task.exception()
