from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.fhir.encounter.entities import Encounter, EncounterStatus
from src.domain.fhir.encounter.repositories import EncounterRepository
from src.infrastructure.db.models.fhir.encounter import Encounter as EncounterModel
from src.infrastructure.db.models.fhir.observation import (
    Observation as ObservationModel,
)


class SQLAlchemyEncounterRepository(EncounterRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, encounter_id: UUID) -> Optional[Encounter]:
        encounter_model = self.db.query(EncounterModel).filter(EncounterModel.id == encounter_id).first()
        if not encounter_model:
            return None

        return Encounter(
            id=encounter_model.id,
            status=EncounterStatus(encounter_model.status) if encounter_model.status else None,
            class_code=encounter_model.class_code,
            subject_patient_id=encounter_model.subject_patient_id,
            period_start=encounter_model.period_start,
            period_end=encounter_model.period_end,
            reason_code=encounter_model.reason_code,
            resource=encounter_model.resource,
            created_at=encounter_model.created_at,
            updated_at=encounter_model.updated_at
        )

    def create(self, encounter: Encounter) -> Encounter:
        encounter_model = EncounterModel(
            status=encounter.status.value if encounter.status else None,
            class_code=encounter.class_code,
            subject_patient_id=encounter.subject_patient_id,
            period_start=encounter.period_start,
            period_end=encounter.period_end,
            reason_code=encounter.reason_code,
            resource=encounter.resource
        )
        self.db.add(encounter_model)
        self.db.commit()
        self.db.refresh(encounter_model)

        return Encounter(
            id=encounter_model.id,
            status=EncounterStatus(encounter_model.status) if encounter_model.status else None,
            class_code=encounter_model.class_code,
            subject_patient_id=encounter_model.subject_patient_id,
            period_start=encounter_model.period_start,
            period_end=encounter_model.period_end,
            reason_code=encounter_model.reason_code,
            resource=encounter_model.resource,
            created_at=encounter_model.created_at,
            updated_at=encounter_model.updated_at
        )

    def update(self, encounter: Encounter) -> Encounter:
        encounter_model = self.db.query(EncounterModel).filter(EncounterModel.id == encounter.id).first()
        if not encounter_model:
            raise ValueError("Encounter not found")

        encounter_model.status = encounter.status.value if encounter.status else None
        encounter_model.class_code = encounter.class_code
        encounter_model.subject_patient_id = encounter.subject_patient_id
        encounter_model.period_start = encounter.period_start
        encounter_model.period_end = encounter.period_end
        encounter_model.reason_code = encounter.reason_code
        encounter_model.resource = encounter.resource

        self.db.commit()
        self.db.refresh(encounter_model)

        return Encounter(
            id=encounter_model.id,
            status=EncounterStatus(encounter_model.status) if encounter_model.status else None,
            class_code=encounter_model.class_code,
            subject_patient_id=encounter_model.subject_patient_id,
            period_start=encounter_model.period_start,
            period_end=encounter_model.period_end,
            reason_code=encounter_model.reason_code,
            resource=encounter_model.resource,
            created_at=encounter_model.created_at,
            updated_at=encounter_model.updated_at
        )

    def delete(self, encounter_id: UUID) -> bool:
        encounter_model = self.db.query(EncounterModel).filter(EncounterModel.id == encounter_id).first()
        if not encounter_model:
            return False

        # Delete dependent observations first to satisfy FK constraints
        self.db.query(ObservationModel).filter(ObservationModel.encounter_id == encounter_id).delete(synchronize_session=False)
        self.db.flush()
        self.db.delete(encounter_model)
        self.db.commit()
        return True

    def search(self, status: Optional[str] = None, subject: Optional[UUID] = None, date: Optional[str] = None) -> List[Encounter]:
        query = self.db.query(EncounterModel)

        if status:
            query = query.filter(EncounterModel.status == status)

        if subject:
            query = query.filter(EncounterModel.subject_patient_id == subject)

        if date:
            query = query.filter(EncounterModel.period_start >= date)

        encounter_models = query.all()

        return [
            Encounter(
                id=em.id,
                status=EncounterStatus(em.status) if em.status else None,
                class_code=em.class_code,
                subject_patient_id=em.subject_patient_id,
                period_start=em.period_start,
                period_end=em.period_end,
                reason_code=em.reason_code,
                resource=em.resource,
                created_at=em.created_at,
                updated_at=em.updated_at
            )
            for em in encounter_models
        ]
