import abc
import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class EventBase(abc.ABC):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    @classmethod
    def get_type(cls):
        return cls.__name__


class DomainEvent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    event_type: str
    event_data: dict

    aggregate_id: uuid.UUID
    aggregate_type: str
    aggregate_version: int

    correlation_id: uuid.UUID
    causation_type: str
    causation_id: uuid.UUID

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def meta_dict(self):
        return self.model_dump(
            mode="json",
            include={
                "event_type",
                "event_data",
                "aggregate_id",
                "aggregate_type",
                "aggregate_version",
                "correlation_id",
                "causation_type",
                "causation_id",
                "created_at",
            },
        )

    def meta_json(self):
        return self.model_dump(
            include={
                "event_type",
                "event_data",
                "aggregate_id",
                "aggregate_type",
                "aggregate_version",
                "correlation_id",
                "causation_type",
                "causation_id",
                "created_at",
            }
        )

    def data_dict(self):
        return self.model_dump(
            mode="json",
            exclude={
                "event_type",
                "event_data",
                "aggregate_id",
                "aggregate_type",
                "aggregate_version",
                "correlation_id",
                "causation_type",
                "causation_id",
                "created_at",
            },
        )

    def data_json(self):
        return self.model_dump_json(
            exclude={
                "event_type",
                "event_data",
                "aggregate_id",
                "aggregate_type",
                "aggregate_version",
                "correlation_id",
                "causation_type",
                "causation_id",
                "created_at",
            }
        )

    def db_model_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def get_type(cls):
        return cls

    @classmethod
    def get_type_str(cls):
        return cls.__name__
