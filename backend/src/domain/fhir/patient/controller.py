from uuid import UUID, uuid4

from src.domain.auth.entities import User
from src.domain.auth.policies import AuthPolicies
from src.domain.fhir.patient.entities import Patient
from src.domain.fhir.patient.repositories import PatientRepository
from src.domain.fhir.patient.view import (
    Bundle,
    BundleEntry,
    PatientCreateRequest,
    PatientResource,
    PatientResponse,
    PatientSearchRequest,
)


class PatientController:
    def __init__(self, patient_repo: PatientRepository):
        self.patient_repo = patient_repo

    def _to_patient_response(self, patient: Patient) -> PatientResponse:
        """Build PatientResponse from stored patient fields + original resource."""
        resource = patient.resource or {}

        # Start with explicit searchable fields, then overlay any provided resource fields
        base = {
            "resourceType": "Patient",
            "id": str(patient.id),
            "identifier": ([{"value": patient.identifier_value}] if patient.identifier_value else []),
            "name": ([{"family": patient.name_family, "given": [patient.name_given]}] if patient.name_family else []),
            "gender": (patient.gender.value if patient.gender else None),
            "birthDate": patient.birth_date,
        }

        combined: dict = {**base, **{k: v for k, v in resource.items() if v is not None}}

        return PatientResponse(**combined)

    def get_patient(self, patient_id: UUID, user: User) -> PatientResponse:
        """Get a specific patient by ID"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        return self._to_patient_response(patient)

    def create_patient(self, request: PatientCreateRequest, user: User) -> PatientResponse:
        """Create a new patient"""
        if not AuthPolicies.can_create_patient(user):
            raise PermissionError("Insufficient permissions")

        # Extract searchable fields
        identifier_value = None
        if request.identifier and len(request.identifier) > 0:
            identifier_value = request.identifier[0].value

        name_family = None
        name_given = None
        if request.name and len(request.name) > 0:
            name_family = request.name[0].family
            name_given = ", ".join(request.name[0].given) if request.name[0].given else None

        # Create domain entity
        # Generate a new UUID for the patient and use Pydantic v2 serialization
        patient = Patient.from_fhir_resource(request.model_dump(), uuid4())

        # Save to repository
        created_patient = self.patient_repo.create(patient)

        return self._to_patient_response(created_patient)

    def search_patients(self, request: PatientSearchRequest, user: User) -> Bundle:
        """Search patients"""
        if not AuthPolicies.can_read_all_resources(user):
            raise PermissionError("Insufficient permissions")

        patients = self.patient_repo.search(
            name=request.name,
            identifier=request.identifier
        )

        entries = []
        for patient in patients:
            # Build resource view from stored resource
            pr = PatientResource(**self._to_patient_response(patient).model_dump())
            entries.append(BundleEntry(resource=pr))

        return Bundle(
            total=len(entries),
            entry=entries
        )

    def update_patient(self, patient_id: UUID, request: PatientCreateRequest, user: User) -> PatientResponse:
        """Update an existing patient"""
        if not AuthPolicies.can_modify_resources(user):
            raise PermissionError("Insufficient permissions")

        patient = Patient.from_fhir_resource(request.model_dump(), patient_id)
        updated = self.patient_repo.update(patient)

        return self._to_patient_response(updated)

    def delete_patient(self, patient_id: UUID, user: User) -> bool:
        """Delete a patient"""
        if not AuthPolicies.can_delete_patient(user):
            raise PermissionError("Insufficient permissions")
        return self.patient_repo.delete(patient_id)
