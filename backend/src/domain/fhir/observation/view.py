from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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
    identifier: Optional[List[Dict[str, Any]]] = None
    instantiatesCanonical: Optional[str] = None
    instantiatesReference: Optional[Reference] = None
    basedOn: Optional[List[Reference]] = None
    triggeredBy: Optional[List[Dict[str, Any]]] = None
    partOf: Optional[List[Reference]] = None
    status: Optional[str] = None
    category: Optional[List[CodeableConcept]] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    focus: Optional[List[Reference]] = None
    encounter: Optional[Reference] = None
    # effective[x]
    effectiveDateTime: Optional[datetime] = None
    effectivePeriod: Optional[Dict[str, Any]] = None
    effectiveTiming: Optional[Dict[str, Any]] = None
    effectiveInstant: Optional[datetime] = None
    issued: Optional[datetime] = None
    performer: Optional[List[Reference]] = None
    # value[x]
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Dict[str, Any]] = None
    valueRatio: Optional[Dict[str, Any]] = None
    valueSampledData: Optional[Dict[str, Any]] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[datetime] = None
    valuePeriod: Optional[Dict[str, Any]] = None
    valueAttachment: Optional[Dict[str, Any]] = None
    valueReference: Optional[Reference] = None
    dataAbsentReason: Optional[CodeableConcept] = None
    interpretation: Optional[List[CodeableConcept]] = None
    note: Optional[List[Dict[str, Any]]] = None
    bodySite: Optional[CodeableConcept] = None
    bodyStructure: Optional[Reference] = None
    method: Optional[CodeableConcept] = None
    specimen: Optional[Reference] = None
    device: Optional[Reference] = None
    referenceRange: Optional[List[Dict[str, Any]]] = None
    hasMember: Optional[List[Reference]] = None
    derivedFrom: Optional[List[Reference]] = None
    component: Optional[List[Dict[str, Any]]] = None

class ObservationCreateRequest(BaseModel):
    resourceType: str = "Observation"
    identifier: Optional[List[Dict[str, Any]]] = None
    instantiatesCanonical: Optional[str] = None
    instantiatesReference: Optional[Reference] = None
    basedOn: Optional[List[Reference]] = None
    triggeredBy: Optional[List[Dict[str, Any]]] = None
    partOf: Optional[List[Reference]] = None
    status: Optional[str] = None
    category: Optional[List[CodeableConcept]] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    focus: Optional[List[Reference]] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    effectivePeriod: Optional[Dict[str, Any]] = None
    effectiveTiming: Optional[Dict[str, Any]] = None
    effectiveInstant: Optional[datetime] = None
    issued: Optional[datetime] = None
    performer: Optional[List[Reference]] = None
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Dict[str, Any]] = None
    valueRatio: Optional[Dict[str, Any]] = None
    valueSampledData: Optional[Dict[str, Any]] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[datetime] = None
    valuePeriod: Optional[Dict[str, Any]] = None
    valueAttachment: Optional[Dict[str, Any]] = None
    valueReference: Optional[Reference] = None
    dataAbsentReason: Optional[CodeableConcept] = None
    interpretation: Optional[List[CodeableConcept]] = None
    note: Optional[List[Dict[str, Any]]] = None
    bodySite: Optional[CodeableConcept] = None
    bodyStructure: Optional[Reference] = None
    method: Optional[CodeableConcept] = None
    specimen: Optional[Reference] = None
    device: Optional[Reference] = None
    referenceRange: Optional[List[Dict[str, Any]]] = None
    hasMember: Optional[List[Reference]] = None
    derivedFrom: Optional[List[Reference]] = None
    component: Optional[List[Dict[str, Any]]] = None

class ObservationResponse(BaseModel):
    resourceType: str = "Observation"
    id: str
    identifier: Optional[List[Dict[str, Any]]] = None
    instantiatesCanonical: Optional[str] = None
    instantiatesReference: Optional[Reference] = None
    basedOn: Optional[List[Reference]] = None
    triggeredBy: Optional[List[Dict[str, Any]]] = None
    partOf: Optional[List[Reference]] = None
    status: Optional[str] = None
    category: Optional[List[CodeableConcept]] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    focus: Optional[List[Reference]] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    effectivePeriod: Optional[Dict[str, Any]] = None
    effectiveTiming: Optional[Dict[str, Any]] = None
    effectiveInstant: Optional[datetime] = None
    issued: Optional[datetime] = None
    performer: Optional[List[Reference]] = None
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueBoolean: Optional[bool] = None
    valueInteger: Optional[int] = None
    valueRange: Optional[Dict[str, Any]] = None
    valueRatio: Optional[Dict[str, Any]] = None
    valueSampledData: Optional[Dict[str, Any]] = None
    valueTime: Optional[str] = None
    valueDateTime: Optional[datetime] = None
    valuePeriod: Optional[Dict[str, Any]] = None
    valueAttachment: Optional[Dict[str, Any]] = None
    valueReference: Optional[Reference] = None
    dataAbsentReason: Optional[CodeableConcept] = None
    interpretation: Optional[List[CodeableConcept]] = None
    note: Optional[List[Dict[str, Any]]] = None
    bodySite: Optional[CodeableConcept] = None
    bodyStructure: Optional[Reference] = None
    method: Optional[CodeableConcept] = None
    specimen: Optional[Reference] = None
    device: Optional[Reference] = None
    referenceRange: Optional[List[Dict[str, Any]]] = None
    hasMember: Optional[List[Reference]] = None
    derivedFrom: Optional[List[Reference]] = None
    component: Optional[List[Dict[str, Any]]] = None

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
