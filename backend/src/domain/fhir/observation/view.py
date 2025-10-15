from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
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

class Quantity(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

class ObservationResource(BaseModel):
    resourceType: str = "Observation"
    id: Optional[str] = None
    status: Optional[str] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    valueQuantity: Optional[Quantity] = None
    valueString: Optional[str] = None

class ObservationCreateRequest(BaseModel):
    resourceType: str = "Observation"
    status: Optional[str] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    valueQuantity: Optional[Quantity] = None
    valueString: Optional[str] = None

class ObservationResponse(BaseModel):
    resourceType: str = "Observation"
    id: str
    status: Optional[str] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    valueQuantity: Optional[Quantity] = None
    valueString: Optional[str] = None

class ObservationSearchRequest(BaseModel):
    code: Optional[str] = None
    date: Optional[str] = None
    subject: Optional[str] = None

class BundleEntry(BaseModel):
    resource: Optional[ObservationResource] = None

class Bundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "searchset"
    total: Optional[int] = None
    entry: Optional[List[BundleEntry]] = None

