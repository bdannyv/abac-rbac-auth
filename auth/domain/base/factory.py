import abc
import typing

from domain.base.command import DomainCommand

T = typing.TypeVar("T")


class AggregateFactory(abc.ABC, typing.Generic[T]):
    @classmethod
    @abc.abstractmethod
    async def create(cls, creation_command: DomainCommand) -> T:
        pass
