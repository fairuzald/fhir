from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class Coding(BaseModel):
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

class Reference(BaseModel):
    reference: Optional[str] = None
    display: Optional[str] = None

class Period(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

class EncounterResource(BaseModel):
    resourceType: str = "Encounter"
    id: Optional[str] = None
    status: Optional[str] = None
    class_: Optional[Coding] = Field(None, alias="class")
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    reasonCode: Optional[List[CodeableConcept]] = None

class EncounterCreateRequest(BaseModel):
    resourceType: str = "Encounter"
    status: Optional[str] = None
    class_: Optional[Coding] = Field(None, alias="class")
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    reasonCode: Optional[List[CodeableConcept]] = None

class EncounterResponse(BaseModel):
    resourceType: str = "Encounter"
    id: str
    status: Optional[str] = None
    class_: Optional[Coding] = Field(None, alias="class")
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    reasonCode: Optional[List[CodeableConcept]] = None

class EncounterSearchRequest(BaseModel):
    status: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None

class BundleEntry(BaseModel):
    resource: Optional[EncounterResource] = None

class Bundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "searchset"
    total: Optional[int] = None
    entry: Optional[List[BundleEntry]] = None

