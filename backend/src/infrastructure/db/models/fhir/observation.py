import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from src.infrastructure.db.base import Base


class Observation(Base):
    __tablename__ = "observation"
    __table_args__ = {'schema': 'fhir'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String)
    code_code = Column(String)
    subject_patient_id = Column(UUID(as_uuid=True), ForeignKey('fhir.patient.id'))
    encounter_id = Column(UUID(as_uuid=True), ForeignKey('fhir.encounter.id', ondelete='CASCADE'))
    effective_datetime = Column(TIMESTAMP(timezone=True))
    value_quantity_value = Column(Numeric)
    value_quantity_unit = Column(String)
    value_string = Column(String)
    resource = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships will be defined after all models are imported
