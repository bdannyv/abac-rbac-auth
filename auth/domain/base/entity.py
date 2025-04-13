import typing

from pydantic import BaseModel


class Entity(BaseModel):
    id: typing.Any
