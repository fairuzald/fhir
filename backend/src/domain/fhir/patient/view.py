from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from uuid import UUID

class Identifier(BaseModel):
    use: Optional[str] = None
    system: Optional[str] = None
    value: str

class HumanName(BaseModel):
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None

class PatientResource(BaseModel):
    resourceType: str = "Patient"
    id: Optional[str] = None
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[HumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None

class PatientCreateRequest(BaseModel):
    resourceType: str = "Patient"
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[HumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None

class PatientResponse(BaseModel):
    resourceType: str = "Patient"
    id: str
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[HumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None

class PatientSearchRequest(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None

class BundleEntry(BaseModel):
    resource: Optional[PatientResource] = None

class Bundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "searchset"
    total: Optional[int] = None
    entry: Optional[List[BundleEntry]] = None

