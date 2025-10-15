from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Numeric, Date, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "auth_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, clinician, read_only
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

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

    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    observations = relationship("Observation", back_populates="patient")

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

    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    observations = relationship("Observation", back_populates="encounter")

class Observation(Base):
    __tablename__ = "observation"
    __table_args__ = {'schema': 'fhir'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String)
    code_code = Column(String)
    subject_patient_id = Column(UUID(as_uuid=True), ForeignKey('fhir.patient.id'))
    encounter_id = Column(UUID(as_uuid=True), ForeignKey('fhir.encounter.id'))
    effective_datetime = Column(TIMESTAMP(timezone=True))
    value_quantity_value = Column(Numeric)
    value_quantity_unit = Column(String)
    value_string = Column(String)
    resource = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="observations")
    encounter = relationship("Encounter", back_populates="observations")

