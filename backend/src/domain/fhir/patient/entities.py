from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

@dataclass
class Identifier:
    use: Optional[str] = None
    system: Optional[str] = None
    value: str = ""

@dataclass
class HumanName:
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None

@dataclass
class Patient:
    id: UUID
    identifier_value: Optional[str]
    name_family: Optional[str]
    name_given: Optional[str]
    gender: Optional[Gender]
    birth_date: Optional[date]
    resource: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    def to_fhir_resource(self) -> Dict[str, Any]:
        """Convert domain entity to FHIR resource"""
        return {
            "resourceType": "Patient",
            "id": str(self.id),
            "identifier": [{"value": self.identifier_value}] if self.identifier_value else [],
            "name": [{"family": self.name_family, "given": [self.name_given]}] if self.name_family else [],
            "gender": self.gender.value if self.gender else None,
            "birthDate": self.birth_date.isoformat() if self.birth_date else None
        }

    @classmethod
    def from_fhir_resource(cls, resource: Dict[str, Any], patient_id: UUID) -> "Patient":
        """Create domain entity from FHIR resource"""
        identifier_value = None
        if resource.get("identifier") and len(resource["identifier"]) > 0:
            identifier_value = resource["identifier"][0].get("value")

        name_family = None
        name_given = None
        if resource.get("name") and len(resource["name"]) > 0:
            name = resource["name"][0]
            name_family = name.get("family")
            name_given = ", ".join(name.get("given", []))

        gender = None
        if resource.get("gender"):
            try:
                gender = Gender(resource["gender"])
            except ValueError:
                gender = Gender.UNKNOWN

        birth_date = None
        if resource.get("birthDate"):
            b = resource["birthDate"]
            if isinstance(b, date):
                birth_date = b
            elif isinstance(b, str):
                birth_date = date.fromisoformat(b)

        # Ensure resource is JSON-serializable (convert date objects to ISO strings)
        resource_serializable = dict(resource)
        if isinstance(resource_serializable.get("birthDate"), date):
            resource_serializable["birthDate"] = resource_serializable["birthDate"].isoformat()

        return cls(
            id=patient_id,
            identifier_value=identifier_value,
            name_family=name_family,
            name_given=name_given,
            gender=gender,
            birth_date=birth_date,
            resource=resource_serializable,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
