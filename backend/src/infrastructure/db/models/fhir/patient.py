import uuid

from sqlalchemy import TIMESTAMP, Column, Date, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from src.infrastructure.db.base import Base


class Patient(Base):
    __tablename__ = "patient"
    __table_args__ = {'schema': 'fhir'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier_value = Column(String)
    name_family = Column(String)
    name_given = Column(String)
    gender = Column(String)  # male, female, other, unknown
    birth_date = Column(Date)
    resource = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships will be defined after all models are imported
