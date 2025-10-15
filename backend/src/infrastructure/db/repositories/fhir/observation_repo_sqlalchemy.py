from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.fhir.observation.entities import Observation, ObservationStatus
from src.domain.fhir.observation.repositories import ObservationRepository
from src.infrastructure.db.models.fhir.encounter import Encounter as EncounterModel
from src.infrastructure.db.models.fhir.observation import (
    Observation as ObservationModel,
)
from src.infrastructure.db.models.fhir.patient import Patient as PatientModel


class SQLAlchemyObservationRepository(ObservationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, observation_id: UUID) -> Optional[Observation]:
        observation_model = self.db.query(ObservationModel).filter(ObservationModel.id == observation_id).first()
        if not observation_model:
            return None

        return Observation(
            id=observation_model.id,
            status=ObservationStatus(observation_model.status) if observation_model.status else None,
            code_code=observation_model.code_code,
            subject_patient_id=observation_model.subject_patient_id,
            encounter_id=observation_model.encounter_id,
            effective_datetime=observation_model.effective_datetime,
            value_quantity_value=float(observation_model.value_quantity_value) if observation_model.value_quantity_value else None,
            value_quantity_unit=observation_model.value_quantity_unit,
            value_string=observation_model.value_string,
            resource=observation_model.resource,
            created_at=observation_model.created_at,
            updated_at=observation_model.updated_at
        )

    def create(self, observation: Observation) -> Observation:
        # Validate referenced Patient exists
        if observation.subject_patient_id:
            patient_exists = (
                self.db.query(PatientModel)
                .filter(PatientModel.id == observation.subject_patient_id)
                .first()
                is not None
            )
            if not patient_exists:
                raise ValueError("Referenced Patient not found")

        # Validate referenced Encounter exists
        if observation.encounter_id:
            encounter_exists = (
                self.db.query(EncounterModel)
                .filter(EncounterModel.id == observation.encounter_id)
                .first()
                is not None
            )
            if not encounter_exists:
                raise ValueError("Referenced Encounter not found")
        observation_model = ObservationModel(
            status=observation.status.value if observation.status else None,
            code_code=observation.code_code,
            subject_patient_id=observation.subject_patient_id,
            encounter_id=observation.encounter_id,
            effective_datetime=observation.effective_datetime,
            value_quantity_value=observation.value_quantity_value,
            value_quantity_unit=observation.value_quantity_unit,
            value_string=observation.value_string,
            resource=observation.resource
        )
        self.db.add(observation_model)
        self.db.commit()
        self.db.refresh(observation_model)

        return Observation(
            id=observation_model.id,
            status=ObservationStatus(observation_model.status) if observation_model.status else None,
            code_code=observation_model.code_code,
            subject_patient_id=observation_model.subject_patient_id,
            encounter_id=observation_model.encounter_id,
            effective_datetime=observation_model.effective_datetime,
            value_quantity_value=float(observation_model.value_quantity_value) if observation_model.value_quantity_value else None,
            value_quantity_unit=observation_model.value_quantity_unit,
            value_string=observation_model.value_string,
            resource=observation_model.resource,
            created_at=observation_model.created_at,
            updated_at=observation_model.updated_at
        )

    def update(self, observation: Observation) -> Observation:
        observation_model = self.db.query(ObservationModel).filter(ObservationModel.id == observation.id).first()
        if not observation_model:
            raise ValueError("Observation not found")

        # Validate referenced Patient exists
        if observation.subject_patient_id:
            patient_exists = (
                self.db.query(PatientModel)
                .filter(PatientModel.id == observation.subject_patient_id)
                .first()
                is not None
            )
            if not patient_exists:
                raise ValueError("Referenced Patient not found")

        # Validate referenced Encounter exists
        if observation.encounter_id:
            encounter_exists = (
                self.db.query(EncounterModel)
                .filter(EncounterModel.id == observation.encounter_id)
                .first()
                is not None
            )
            if not encounter_exists:
                raise ValueError("Referenced Encounter not found")

        observation_model.status = observation.status.value if observation.status else None
        observation_model.code_code = observation.code_code
        observation_model.subject_patient_id = observation.subject_patient_id
        observation_model.encounter_id = observation.encounter_id
        observation_model.effective_datetime = observation.effective_datetime
        observation_model.value_quantity_value = observation.value_quantity_value
        observation_model.value_quantity_unit = observation.value_quantity_unit
        observation_model.value_string = observation.value_string
        observation_model.resource = observation.resource

        self.db.commit()
        self.db.refresh(observation_model)

        return Observation(
            id=observation_model.id,
            status=ObservationStatus(observation_model.status) if observation_model.status else None,
            code_code=observation_model.code_code,
            subject_patient_id=observation_model.subject_patient_id,
            encounter_id=observation_model.encounter_id,
            effective_datetime=observation_model.effective_datetime,
            value_quantity_value=float(observation_model.value_quantity_value) if observation_model.value_quantity_value else None,
            value_quantity_unit=observation_model.value_quantity_unit,
            value_string=observation_model.value_string,
            resource=observation_model.resource,
            created_at=observation_model.created_at,
            updated_at=observation_model.updated_at
        )

    def delete(self, observation_id: UUID) -> bool:
        observation_model = self.db.query(ObservationModel).filter(ObservationModel.id == observation_id).first()
        if not observation_model:
            return False

        self.db.delete(observation_model)
        self.db.commit()
        return True

    def search(self, code: Optional[str] = None, date: Optional[str] = None, subject: Optional[UUID] = None) -> List[Observation]:
        query = self.db.query(ObservationModel)

        if code:
            query = query.filter(ObservationModel.code_code == code)

        if subject:
            query = query.filter(ObservationModel.subject_patient_id == subject)

        if date:
            query = query.filter(ObservationModel.effective_datetime >= date)

        observation_models = query.all()

        return [
            Observation(
                id=om.id,
                status=ObservationStatus(om.status) if om.status else None,
                code_code=om.code_code,
                subject_patient_id=om.subject_patient_id,
                encounter_id=om.encounter_id,
                effective_datetime=om.effective_datetime,
                value_quantity_value=float(om.value_quantity_value) if om.value_quantity_value else None,
                value_quantity_unit=om.value_quantity_unit,
                value_string=om.value_string,
                resource=om.resource,
                created_at=om.created_at,
                updated_at=om.updated_at
            )
            for om in observation_models
        ]
