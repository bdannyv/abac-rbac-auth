import sqlalchemy as sa
from core.data_storage import Base


class DomainEvent(Base):
    __tablename__ = "domain_event"
    __table_args__ = (
        sa.Index("domain_event_aggregate_fk", "aggregate_id"),
        sa.Index("domain_event_aggregate_version_idx", "aggregate_version"),
        sa.UniqueConstraint("aggregate_id", "aggregate_version", name="uq_aggregate_version"),
    )

    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    event_type = sa.Column(sa.VARCHAR(50), nullable=False)
    event_data = sa.Column(sa.JSON, nullable=False)

    aggregate_id = sa.Column(sa.UUID(as_uuid=True), nullable=False)
    aggregate_type = sa.Column(sa.VARCHAR(50), nullable=False)
    aggregate_version = sa.Column(sa.Integer, nullable=False)

    correlation_id = sa.Column(sa.UUID(as_uuid=True), nullable=False)

    causation_id = sa.Column(sa.UUID(as_uuid=True))
    causation_type = sa.Column(sa.VARCHAR(50), nullable=False)

    created_at = sa.Column(sa.DateTime, nullable=False)
