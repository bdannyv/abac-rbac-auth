import enum
import uuid

import pydantic


class ConsistencyType(enum.StrEnum):
    PESSIMISTIC = "pessimistic"
    OPTIMISTIC = "optimistic"


class DomainCommand(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    consistency_type: ConsistencyType = ConsistencyType.OPTIMISTIC
