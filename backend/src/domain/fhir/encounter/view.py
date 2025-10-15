from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
    identifier: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    class_: Optional[List[CodeableConcept]] = Field(default=None, alias="class")
    priority: Optional[CodeableConcept] = None
    type: Optional[List[CodeableConcept]] = None
    serviceType: Optional[List[Dict[str, Any]]] = None  # CodeableReference(HealthcareService)
    subject: Optional[Reference] = None
    subjectStatus: Optional[CodeableConcept] = None
    episodeOfCare: Optional[List[Reference]] = None
    basedOn: Optional[List[Reference]] = None
    careTeam: Optional[List[Reference]] = None
    partOf: Optional[Reference] = None
    serviceProvider: Optional[Reference] = None
    class Participant(BaseModel):
        type: Optional[List[CodeableConcept]] = None
        period: Optional[Period] = None
        actor: Optional[Reference] = None
    participant: Optional[List[Participant]] = None
    appointment: Optional[List[Reference]] = None
    virtualService: Optional[List[Dict[str, Any]]] = None
    actualPeriod: Optional[Period] = None
    plannedStartDate: Optional[datetime] = None
    plannedEndDate: Optional[datetime] = None
    length: Optional[Dict[str, Any]] = None  # Duration
    class Reason(BaseModel):
        use: Optional[List[CodeableConcept]] = None
        value: Optional[List[Reference]] = None  # CodeableReference
    reason: Optional[List[Reason]] = None
    class Diagnosis(BaseModel):
        condition: Optional[List[Reference]] = None
        use: Optional[List[CodeableConcept]] = None
    diagnosis: Optional[List[Diagnosis]] = None
    account: Optional[List[Reference]] = None
    dietPreference: Optional[List[CodeableConcept]] = None
    specialArrangement: Optional[List[CodeableConcept]] = None
    specialCourtesy: Optional[List[CodeableConcept]] = None
    class Admission(BaseModel):
        preAdmissionIdentifier: Optional[Dict[str, Any]] = None  # Identifier
        origin: Optional[Reference] = None
        admitSource: Optional[CodeableConcept] = None
        reAdmission: Optional[CodeableConcept] = None
        destination: Optional[Reference] = None
        dischargeDisposition: Optional[CodeableConcept] = None
    admission: Optional[Admission] = None
    class Location(BaseModel):
        location: Reference
        status: Optional[str] = None
        form: Optional[CodeableConcept] = None
        period: Optional[Period] = None
    location: Optional[List[Location]] = None

class EncounterCreateRequest(BaseModel):
    resourceType: str = "Encounter"
    identifier: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    class_: Optional[List[CodeableConcept]] = Field(default=None, alias="class")
    priority: Optional[CodeableConcept] = None
    type: Optional[List[CodeableConcept]] = None
    serviceType: Optional[List[Dict[str, Any]]] = None
    subject: Optional[Reference] = None
    subjectStatus: Optional[CodeableConcept] = None
    episodeOfCare: Optional[List[Reference]] = None
    basedOn: Optional[List[Reference]] = None
    careTeam: Optional[List[Reference]] = None
    partOf: Optional[Reference] = None
    serviceProvider: Optional[Reference] = None
    participant: Optional[List[EncounterResource.Participant]] = None
    appointment: Optional[List[Reference]] = None
    virtualService: Optional[List[Dict[str, Any]]] = None
    actualPeriod: Optional[Period] = None
    plannedStartDate: Optional[datetime] = None
    plannedEndDate: Optional[datetime] = None
    length: Optional[Dict[str, Any]] = None
    reason: Optional[List[EncounterResource.Reason]] = None
    diagnosis: Optional[List[EncounterResource.Diagnosis]] = None
    account: Optional[List[Reference]] = None
    dietPreference: Optional[List[CodeableConcept]] = None
    specialArrangement: Optional[List[CodeableConcept]] = None
    specialCourtesy: Optional[List[CodeableConcept]] = None
    admission: Optional[EncounterResource.Admission] = None
    location: Optional[List[EncounterResource.Location]] = None

class EncounterResponse(BaseModel):
    resourceType: str = "Encounter"
    id: str
    identifier: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    class_: Optional[List[CodeableConcept]] = Field(default=None, alias="class")
    priority: Optional[CodeableConcept] = None
    type: Optional[List[CodeableConcept]] = None
    serviceType: Optional[List[Dict[str, Any]]] = None
    subject: Optional[Reference] = None
    subjectStatus: Optional[CodeableConcept] = None
    episodeOfCare: Optional[List[Reference]] = None
    basedOn: Optional[List[Reference]] = None
    careTeam: Optional[List[Reference]] = None
    partOf: Optional[Reference] = None
    serviceProvider: Optional[Reference] = None
    participant: Optional[List[EncounterResource.Participant]] = None
    appointment: Optional[List[Reference]] = None
    virtualService: Optional[List[Dict[str, Any]]] = None
    actualPeriod: Optional[Period] = None
    plannedStartDate: Optional[datetime] = None
    plannedEndDate: Optional[datetime] = None
    length: Optional[Dict[str, Any]] = None
    reason: Optional[List[EncounterResource.Reason]] = None
    diagnosis: Optional[List[EncounterResource.Diagnosis]] = None
    account: Optional[List[Reference]] = None
    dietPreference: Optional[List[CodeableConcept]] = None
    specialArrangement: Optional[List[CodeableConcept]] = None
    specialCourtesy: Optional[List[CodeableConcept]] = None
    admission: Optional[EncounterResource.Admission] = None
    location: Optional[List[EncounterResource.Location]] = None

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
