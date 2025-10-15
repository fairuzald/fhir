from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID


class ObservationStatus(str, Enum):
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"

@dataclass
class Coding:
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

@dataclass
class CodeableConcept:
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

@dataclass
class Reference:
    reference: Optional[str] = None
    display: Optional[str] = None

@dataclass
class Quantity:
    value: Optional[float] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

@dataclass
class Observation:
    id: UUID
    status: Optional[ObservationStatus]
    code_code: Optional[str]
    subject_patient_id: Optional[UUID]
    encounter_id: Optional[UUID]
    effective_datetime: Optional[datetime]
    value_quantity_value: Optional[float]
    value_quantity_unit: Optional[str]
    value_string: Optional[str]
    resource: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    def to_fhir_resource(self) -> Dict[str, Any]:
        """Convert domain entity to FHIR resource"""
        return {
            "resourceType": "Observation",
            "id": str(self.id),
            "status": self.status.value if self.status else None,
            "code": {"coding": [{"code": self.code_code}]} if self.code_code else None,
            "subject": {"reference": f"Patient/{self.subject_patient_id}"} if self.subject_patient_id else None,
            "encounter": {"reference": f"Encounter/{self.encounter_id}"} if self.encounter_id else None,
            "effectiveDateTime": self.effective_datetime.isoformat() if self.effective_datetime else None,
            "valueQuantity": {
                "value": self.value_quantity_value,
                "unit": self.value_quantity_unit
            } if self.value_quantity_value is not None else None,
            "valueString": self.value_string
        }

    @classmethod
    def from_fhir_resource(cls, resource: Dict[str, Any], observation_id: UUID) -> "Observation":
        """Create domain entity from FHIR resource"""
        status = None
        if resource.get("status"):
            try:
                status = ObservationStatus(resource["status"])
            except ValueError:
                status = ObservationStatus.UNKNOWN

        code_code = None
        if resource.get("code") and resource["code"].get("coding"):
            code_code = resource["code"]["coding"][0].get("code")

        subject_patient_id = None
        if resource.get("subject") and resource["subject"].get("reference"):
            try:
                subject_patient_id = UUID(resource["subject"]["reference"].split("/")[-1])
            except (ValueError, IndexError):
                pass

        encounter_id = None
        if resource.get("encounter") and resource["encounter"].get("reference"):
            try:
                encounter_id = UUID(resource["encounter"]["reference"].split("/")[-1])
            except (ValueError, IndexError):
                pass

        effective_datetime = None
        if resource.get("effectiveDateTime"):
            raw_effective = resource["effectiveDateTime"]
            if isinstance(raw_effective, str):
                # Support Z suffix and timezone-aware strings
                effective_datetime = datetime.fromisoformat(raw_effective.replace("Z", "+00:00"))
            elif isinstance(raw_effective, datetime):
                effective_datetime = raw_effective
            elif isinstance(raw_effective, date):
                effective_datetime = datetime.combine(raw_effective, datetime.min.time())

        value_quantity_value = None
        value_quantity_unit = None
        if resource.get("valueQuantity"):
            value_quantity_value = resource["valueQuantity"].get("value")
            value_quantity_unit = resource["valueQuantity"].get("unit")

        value_string = resource.get("valueString")

        # Ensure JSON-serializable resource (convert datetimes to ISO strings)
        normalized_resource = dict(resource)
        if effective_datetime is not None:
            normalized_resource["effectiveDateTime"] = effective_datetime.isoformat()

        return cls(
            id=observation_id,
            status=status,
            code_code=code_code,
            subject_patient_id=subject_patient_id,
            encounter_id=encounter_id,
            effective_datetime=effective_datetime,
            value_quantity_value=value_quantity_value,
            value_quantity_unit=value_quantity_unit,
            value_string=value_string,
            resource=normalized_resource,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
