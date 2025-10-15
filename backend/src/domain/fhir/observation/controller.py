from uuid import UUID

from src.domain.auth.entities import User
from src.domain.auth.policies import AuthPolicies
from src.domain.fhir.observation.entities import Observation
from src.domain.fhir.observation.repositories import ObservationRepository
from src.domain.fhir.observation.view import (
    Bundle,
    BundleEntry,
    ObservationCreateRequest,
    ObservationResource,
    ObservationResponse,
    ObservationSearchRequest,
)


class ObservationController:
    def __init__(self, observation_repo: ObservationRepository):
        self.observation_repo = observation_repo

    def get_observation(self, observation_id: UUID, user: User) -> ObservationResponse:
        """Get a specific observation by ID"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        observation = self.observation_repo.get_by_id(observation_id)
        if not observation:
            raise ValueError("Observation not found")

        return ObservationResponse(
            resourceType="Observation",
            id=str(observation.id),
            status=observation.status.value if observation.status else None,
            code={"coding": [{"code": observation.code_code}]} if observation.code_code else None,
            subject={"reference": f"Patient/{observation.subject_patient_id}"} if observation.subject_patient_id else None,
            encounter={"reference": f"Encounter/{observation.encounter_id}"} if observation.encounter_id else None,
            effectiveDateTime=observation.effective_datetime,
            valueQuantity={
                "value": observation.value_quantity_value,
                "unit": observation.value_quantity_unit
            } if observation.value_quantity_value is not None else None,
            valueString=observation.value_string
        )

    def create_observation(self, request: ObservationCreateRequest, user: User) -> ObservationResponse:
        """Create a new observation"""
        if not AuthPolicies.can_create_observation(user):
            raise PermissionError("Insufficient permissions")

        # Create domain entity
        observation = Observation.from_fhir_resource(request.dict(), UUID())

        # Save to repository
        created_observation = self.observation_repo.create(observation)

        return ObservationResponse(
            resourceType="Observation",
            id=str(created_observation.id),
            status=created_observation.status.value if created_observation.status else None,
            code={"coding": [{"code": created_observation.code_code}]} if created_observation.code_code else None,
            subject={"reference": f"Patient/{created_observation.subject_patient_id}"} if created_observation.subject_patient_id else None,
            encounter={"reference": f"Encounter/{created_observation.encounter_id}"} if created_observation.encounter_id else None,
            effectiveDateTime=created_observation.effective_datetime,
            valueQuantity={
                "value": created_observation.value_quantity_value,
                "unit": created_observation.value_quantity_unit
            } if created_observation.value_quantity_value is not None else None,
            valueString=created_observation.value_string
        )

    def search_observations(self, request: ObservationSearchRequest, user: User) -> Bundle:
        """Search observations"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        subject_uuid = None
        if request.subject:
            try:
                subject_uuid = UUID(request.subject.split("/")[-1])
            except (ValueError, IndexError):
                pass

        observations = self.observation_repo.search(
            code=request.code,
            date=request.date,
            subject=subject_uuid
        )

        entries = []
        for observation in observations:
            entries.append(BundleEntry(
                resource=ObservationResource(
                    resourceType="Observation",
                    id=str(observation.id),
                    status=observation.status.value if observation.status else None,
                    code={"coding": [{"code": observation.code_code}]} if observation.code_code else None,
                    subject={"reference": f"Patient/{observation.subject_patient_id}"} if observation.subject_patient_id else None,
                    encounter={"reference": f"Encounter/{observation.encounter_id}"} if observation.encounter_id else None,
                    effectiveDateTime=observation.effective_datetime,
                    valueQuantity={
                        "value": observation.value_quantity_value,
                        "unit": observation.value_quantity_unit
                    } if observation.value_quantity_value is not None else None,
                    valueString=observation.value_string
                )
            ))

        return Bundle(
            total=len(entries),
            entry=entries
        )

    def update_observation(self, observation_id: UUID, request: ObservationCreateRequest, user: User) -> ObservationResponse:
        """Update an existing observation"""
        if not AuthPolicies.can_modify_observation(user.role.value):
            raise PermissionError("Insufficient permissions")

        observation = Observation.from_fhir_resource(request.dict(), observation_id)
        updated = self.observation_repo.update(observation)

        return ObservationResponse(
            resourceType="Observation",
            id=str(updated.id),
            status=updated.status.value if updated.status else None,
            code={"coding": [{"code": updated.code_code}]} if updated.code_code else None,
            subject={"reference": f"Patient/{updated.subject_patient_id}"} if updated.subject_patient_id else None,
            encounter={"reference": f"Encounter/{updated.encounter_id}"} if updated.encounter_id else None,
            effectiveDateTime=updated.effective_datetime,
            valueQuantity={
                "value": updated.value_quantity_value,
                "unit": updated.value_quantity_unit
            } if updated.value_quantity_value is not None else None,
            valueString=updated.value_string
        )

    def delete_observation(self, observation_id: UUID, user: User) -> bool:
        """Delete an observation"""
        if not AuthPolicies.can_delete_observation(user.role.value):
            raise PermissionError("Insufficient permissions")
        return self.observation_repo.delete(observation_id)
