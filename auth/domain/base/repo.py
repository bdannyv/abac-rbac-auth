import abc
import typing
import uuid

T = typing.TypeVar("T")


class AggregateRepository(abc.ABC, typing.Generic[T]):
    @classmethod
    @abc.abstractmethod
    async def get(cls, aggregate_id: uuid.UUID) -> T:
        pass

    @classmethod
    @abc.abstractmethod
    async def save(cls, aggregate: T):
        pass
