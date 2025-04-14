import abc
import typing

from core.data_storage import session_factory
from sqlalchemy.ext.asyncio import AsyncSession

DomainEventType = typing.TypeVar("DomainEventType")


class EventHandlerGroup(abc.ABC, typing.Generic[DomainEventType]):
    """Group of related event handlers that are executed sequentially"""

    handlers: list[typing.Callable[[DomainEventType, AsyncSession], typing.Any]]

    @classmethod
    def get_type_str(cls):
        return cls.__name__

    @classmethod
    async def handle_event(cls, event: DomainEventType):
        async with session_factory() as session:
            for handler in cls.handlers:
                await handler(event, session)
