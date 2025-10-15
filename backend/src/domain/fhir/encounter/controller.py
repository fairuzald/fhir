from uuid import UUID

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

    async def get_encounter(self, encounter_id: UUID, user: User) -> EncounterResponse:
        """Get a specific encounter by ID"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        encounter = await self.encounter_repo.get_by_id(encounter_id)
        if not encounter:
            raise ValueError("Encounter not found")

        return EncounterResponse(
            resourceType="Encounter",
            id=str(encounter.id),
            status=encounter.status.value if encounter.status else None,
            class_={"code": encounter.class_code} if encounter.class_code else None,
            subject={"reference": f"Patient/{encounter.subject_patient_id}"} if encounter.subject_patient_id else None,
            period={
                "start": encounter.period_start,
                "end": encounter.period_end
            } if encounter.period_start or encounter.period_end else None,
            reasonCode=[{"coding": [{"code": encounter.reason_code}]}] if encounter.reason_code else []
        )

    async def create_encounter(self, request: EncounterCreateRequest, user: User) -> EncounterResponse:
        """Create a new encounter"""
        if not AuthPolicies.can_create_encounter(user):
            raise PermissionError("Insufficient permissions")

        # Create domain entity
        encounter = Encounter.from_fhir_resource(request.dict(), UUID())

        # Save to repository
        created_encounter = await self.encounter_repo.create(encounter)

        return EncounterResponse(
            resourceType="Encounter",
            id=str(created_encounter.id),
            status=created_encounter.status.value if created_encounter.status else None,
            class_={"code": created_encounter.class_code} if created_encounter.class_code else None,
            subject={"reference": f"Patient/{created_encounter.subject_patient_id}"} if created_encounter.subject_patient_id else None,
            period={
                "start": created_encounter.period_start,
                "end": created_encounter.period_end
            } if created_encounter.period_start or created_encounter.period_end else None,
            reasonCode=[{"coding": [{"code": created_encounter.reason_code}]}] if created_encounter.reason_code else []
        )

    async def search_encounters(self, request: EncounterSearchRequest, user: User) -> Bundle:
        """Search encounters"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        subject_uuid = None
        if request.subject:
            try:
                subject_uuid = UUID(request.subject.split("/")[-1])
            except (ValueError, IndexError):
                pass

        encounters = await self.encounter_repo.search(
            status=request.status,
            subject=subject_uuid,
            date=request.date
        )

        entries = []
        for encounter in encounters:
            entries.append(BundleEntry(
                resource=EncounterResource(
                    resourceType="Encounter",
                    id=str(encounter.id),
                    status=encounter.status.value if encounter.status else None,
                    class_={"code": encounter.class_code} if encounter.class_code else None,
                    subject={"reference": f"Patient/{encounter.subject_patient_id}"} if encounter.subject_patient_id else None,
                    period={
                        "start": encounter.period_start,
                        "end": encounter.period_end
                    } if encounter.period_start or encounter.period_end else None,
                    reasonCode=[{"coding": [{"code": encounter.reason_code}]}] if encounter.reason_code else []
                )
            ))

        return Bundle(
            total=len(entries),
            entry=entries
        )
