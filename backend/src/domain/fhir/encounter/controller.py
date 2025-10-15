from uuid import UUID, uuid4

from src.domain.auth.entities import User
from src.domain.auth.policies import AuthPolicies
from src.domain.fhir.encounter.entities import Encounter
from src.domain.fhir.encounter.repositories import EncounterRepository
from src.domain.fhir.encounter.view import (
    Bundle,
    BundleEntry,
    EncounterCreateRequest,
    EncounterResource,
    EncounterResponse,
    EncounterSearchRequest,
)


class EncounterController:
    def __init__(self, encounter_repo: EncounterRepository):
        self.encounter_repo = encounter_repo

    def _to_encounter_response(self, encounter: Encounter) -> EncounterResponse:
        """Build EncounterResponse from stored encounter fields + original resource."""
        resource = encounter.resource or {}

        base = {
            "resourceType": "Encounter",
            "id": str(encounter.id),
            "status": (encounter.status.value if encounter.status else None),
            # Map simple class code into CodeableConcept list when available
            "class": ([{"coding": [{"code": encounter.class_code}]}] if encounter.class_code else None),
            "subject": ({"reference": f"Patient/{encounter.subject_patient_id}"} if encounter.subject_patient_id else None),
            "actualPeriod": ({
                "start": encounter.period_start,
                "end": encounter.period_end,
            } if encounter.period_start or encounter.period_end else None),
            # Older shape compatibility
            "period": ({
                "start": encounter.period_start,
                "end": encounter.period_end,
            } if encounter.period_start or encounter.period_end else None),
            "reason": ([{"value": [{"reference": encounter.reason_code}]}] if encounter.reason_code else None),
        }

        # Overlay original resource fields (they may include richer FHIR content)
        combined = {**{k: v for k, v in base.items() if v is not None}, **{k: v for k, v in resource.items() if v is not None}}

        return EncounterResponse(**combined)

    def get_encounter(self, encounter_id: UUID, user: User) -> EncounterResponse:
        """Get a specific encounter by ID"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        encounter = self.encounter_repo.get_by_id(encounter_id)
        if not encounter:
            raise ValueError("Encounter not found")

        return self._to_encounter_response(encounter)

    def create_encounter(self, request: EncounterCreateRequest, user: User) -> EncounterResponse:
        """Create a new encounter"""
        if not AuthPolicies.can_create_encounter(user):
            raise PermissionError("Insufficient permissions")

        # Create domain entity
        encounter = Encounter.from_fhir_resource(request.model_dump(), uuid4())

        # Save to repository
        created_encounter = self.encounter_repo.create(encounter)

        return self._to_encounter_response(created_encounter)

    def search_encounters(self, request: EncounterSearchRequest, user: User) -> Bundle:
        """Search encounters"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        subject_uuid = None
        if request.subject:
            try:
                subject_uuid = UUID(request.subject.split("/")[-1])
            except (ValueError, IndexError):
                pass

        encounters = self.encounter_repo.search(
            status=request.status,
            subject=subject_uuid,
            date=request.date
        )

        entries = []
        for encounter in encounters:
            er = EncounterResource(**self._to_encounter_response(encounter).model_dump())
            entries.append(BundleEntry(resource=er))

        return Bundle(
            total=len(entries),
            entry=entries
        )

    def update_encounter(self, encounter_id: UUID, request: EncounterCreateRequest, user: User) -> EncounterResponse:
        """Update an existing encounter"""
        if not AuthPolicies.can_modify_encounter(user):
            raise PermissionError("Insufficient permissions")

        encounter = Encounter.from_fhir_resource(request.model_dump(), encounter_id)
        updated = self.encounter_repo.update(encounter)

        return self._to_encounter_response(updated)

    def delete_encounter(self, encounter_id: UUID, user: User) -> bool:
        """Delete an encounter"""
        if not AuthPolicies.can_delete_encounter(user):
            raise PermissionError("Insufficient permissions")
        return self.encounter_repo.delete(encounter_id)
