from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.fhir.patient.entities import Patient, Gender
from src.domain.fhir.patient.repositories import PatientRepository
from src.infrastructure.db.models.fhir.patient import Patient as PatientModel

class SQLAlchemyPatientRepository(PatientRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        patient_model = self.db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if not patient_model:
            return None

        return Patient(
            id=patient_model.id,
            identifier_value=patient_model.identifier_value,
            name_family=patient_model.name_family,
            name_given=patient_model.name_given,
            gender=Gender(patient_model.gender) if patient_model.gender else None,
            birth_date=patient_model.birth_date,
            resource=patient_model.resource,
            created_at=patient_model.created_at,
            updated_at=patient_model.updated_at
        )

    def create(self, patient: Patient) -> Patient:
        patient_model = PatientModel(
            identifier_value=patient.identifier_value,
            name_family=patient.name_family,
            name_given=patient.name_given,
            gender=patient.gender.value if patient.gender else None,
            birth_date=patient.birth_date,
            resource=patient.resource
        )
        self.db.add(patient_model)
        self.db.commit()
        self.db.refresh(patient_model)

        return Patient(
            id=patient_model.id,
            identifier_value=patient_model.identifier_value,
            name_family=patient_model.name_family,
            name_given=patient_model.name_given,
            gender=Gender(patient_model.gender) if patient_model.gender else None,
            birth_date=patient_model.birth_date,
            resource=patient_model.resource,
            created_at=patient_model.created_at,
            updated_at=patient_model.updated_at
        )

    def update(self, patient: Patient) -> Patient:
        patient_model = self.db.query(PatientModel).filter(PatientModel.id == patient.id).first()
        if not patient_model:
            raise ValueError("Patient not found")

        patient_model.identifier_value = patient.identifier_value
        patient_model.name_family = patient.name_family
        patient_model.name_given = patient.name_given
        patient_model.gender = patient.gender.value if patient.gender else None
        patient_model.birth_date = patient.birth_date
        patient_model.resource = patient.resource

        self.db.commit()
        self.db.refresh(patient_model)

        return Patient(
            id=patient_model.id,
            identifier_value=patient_model.identifier_value,
            name_family=patient_model.name_family,
            name_given=patient_model.name_given,
            gender=Gender(patient_model.gender) if patient_model.gender else None,
            birth_date=patient_model.birth_date,
            resource=patient_model.resource,
            created_at=patient_model.created_at,
            updated_at=patient_model.updated_at
        )

    def delete(self, patient_id: UUID) -> bool:
        patient_model = self.db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if not patient_model:
            return False

        self.db.delete(patient_model)
        self.db.commit()
        return True

    def search(self, name: Optional[str] = None, identifier: Optional[str] = None) -> List[Patient]:
        query = self.db.query(PatientModel)

        if name:
            query = query.filter(
                (PatientModel.name_family.ilike(f"%{name}%")) |
                (PatientModel.name_given.ilike(f"%{name}%"))
            )

        if identifier:
            query = query.filter(PatientModel.identifier_value.ilike(f"%{identifier}%"))

        patient_models = query.all()

        return [
            Patient(
                id=pm.id,
                identifier_value=pm.identifier_value,
                name_family=pm.name_family,
                name_given=pm.name_given,
                gender=Gender(pm.gender) if pm.gender else None,
                birth_date=pm.birth_date,
                resource=pm.resource,
                created_at=pm.created_at,
                updated_at=pm.updated_at
            )
            for pm in patient_models
        ]
