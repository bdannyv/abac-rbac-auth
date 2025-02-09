from sqlalchemy import UUID, VARCHAR, Boolean, Column, text

from infra.data_storage import Base


class User(Base):
    __table__ = "app_user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(VARCHAR(32), nullable=False)
    last_name = Column(VARCHAR(64), nullable=False)
    email = Column(VARCHAR(320), nullable=True, unique=True)
    password = Column(VARCHAR(64), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
