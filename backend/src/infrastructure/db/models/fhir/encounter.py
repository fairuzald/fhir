from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from src.infrastructure.db.base import Base

class Encounter(Base):
    __tablename__ = "encounter"
    __table_args__ = {'schema': 'fhir'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String)
    class_code = Column(String)
    subject_patient_id = Column(UUID(as_uuid=True), ForeignKey('fhir.patient.id'))
    period_start = Column(TIMESTAMP(timezone=True))
    period_end = Column(TIMESTAMP(timezone=True))
    reason_code = Column(String)
    resource = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships will be defined after all models are imported
