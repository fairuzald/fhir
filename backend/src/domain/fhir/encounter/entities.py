from enum import Enum
from dataclasses import dataclass
from datetime import datetime, date
from uuid import UUID
from typing import Optional, List, Dict, Any

class EncounterStatus(str, Enum):
    PLANNED = "planned"
    ARRIVED = "arrived"
    TRIAGED = "triaged"
    IN_PROGRESS = "in-progress"
    ONLEAVE = "onleave"
    FINISHED = "finished"
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
class Period:
    start: Optional[datetime] = None
    end: Optional[datetime] = None

@dataclass
class Encounter:
    id: UUID
    status: Optional[EncounterStatus]
    class_code: Optional[str]
    subject_patient_id: Optional[UUID]
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    reason_code: Optional[str]
    resource: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    def to_fhir_resource(self) -> Dict[str, Any]:
        """Convert domain entity to FHIR resource"""
        return {
            "resourceType": "Encounter",
            "id": str(self.id),
            "status": self.status.value if self.status else None,
            "class": {"code": self.class_code} if self.class_code else None,
            "subject": {"reference": f"Patient/{self.subject_patient_id}"} if self.subject_patient_id else None,
            "period": {
                "start": self.period_start.isoformat() if self.period_start else None,
                "end": self.period_end.isoformat() if self.period_end else None
            } if self.period_start or self.period_end else None,
            "reasonCode": [{"coding": [{"code": self.reason_code}]}] if self.reason_code else []
        }

    @classmethod
    def from_fhir_resource(cls, resource: Dict[str, Any], encounter_id: UUID) -> "Encounter":
        """Create domain entity from FHIR resource"""
        status = None
        if resource.get("status"):
            try:
                status = EncounterStatus(resource["status"])
            except ValueError:
                status = EncounterStatus.UNKNOWN

        class_code = None
        if resource.get("class") and resource["class"].get("code"):
            class_code = resource["class"]["code"]

        subject_patient_id = None
        if resource.get("subject") and resource["subject"].get("reference"):
            try:
                subject_patient_id = UUID(resource["subject"]["reference"].split("/")[-1])
            except (ValueError, IndexError):
                pass

        period_start = None
        period_end = None
        if resource.get("period"):
            period = resource["period"]
            if period.get("start"):
                period_start = datetime.fromisoformat(period["start"].replace("Z", "+00:00"))
            if period.get("end"):
                period_end = datetime.fromisoformat(period["end"].replace("Z", "+00:00"))

        reason_code = None
        if resource.get("reasonCode") and len(resource["reasonCode"]) > 0:
            reason = resource["reasonCode"][0]
            if reason.get("coding") and len(reason["coding"]) > 0:
                reason_code = reason["coding"][0].get("code")

        return cls(
            id=encounter_id,
            status=status,
            class_code=class_code,
            subject_patient_id=subject_patient_id,
            period_start=period_start,
            period_end=period_end,
            reason_code=reason_code,
            resource=resource,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

