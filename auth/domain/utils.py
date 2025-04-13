import typing

import pydantic

NonEmptyStr = typing.Annotated[str, pydantic.Field(min_length=1)]
