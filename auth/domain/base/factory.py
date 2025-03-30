import abc
import typing

T = typing.TypeVar("T")


class AggregateFactory(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def create(self, *args, **kwargs) -> T:
        pass
