from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class Identifier(BaseModel):
    use: Optional[str] = None
    system: Optional[str] = None
    value: str

class HumanName(BaseModel):
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None

class ContactPoint(BaseModel):
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None

class Address(BaseModel):
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None

class Attachment(BaseModel):
    contentType: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None

class Coding(BaseModel):
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

class Period(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None

class Reference(BaseModel):
    reference: Optional[str] = None
    display: Optional[str] = None

class PatientResource(BaseModel):
    resourceType: str = "Patient"
    id: Optional[str] = None
    identifier: List[Identifier] = Field(default_factory=list)
    active: Optional[bool] = None
    name: List[HumanName] = Field(default_factory=list)
    telecom: List[ContactPoint] = Field(default_factory=list)
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[str] = None
    address: List[Address] = Field(default_factory=list)
    maritalStatus: Optional[CodeableConcept] = None
    multipleBirthBoolean: Optional[bool] = None
    multipleBirthInteger: Optional[int] = None
    photo: List[Attachment] = Field(default_factory=list)
    # contact
    class Contact(BaseModel):
        relationship: Optional[List[CodeableConcept]] = None
        name: Optional[HumanName] = None
        telecom: Optional[List[ContactPoint]] = None
        address: Optional[Address] = None
        gender: Optional[str] = None
        organization: Optional[Reference] = None
        period: Optional[Period] = None
    contact: List[Contact] = Field(default_factory=list)
    # communication
    class Communication(BaseModel):
        language: CodeableConcept
        preferred: Optional[bool] = None
    communication: List[Communication] = Field(default_factory=list)
    generalPractitioner: List[Reference] = Field(default_factory=list)
    managingOrganization: Optional[Reference] = None
    # link
    class Link(BaseModel):
        other: Reference
        type: str
    link: List[Link] = Field(default_factory=list)

class PatientCreateRequest(BaseModel):
    resourceType: str = "Patient"
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[str] = None
    address: Optional[List[Address]] = None
    maritalStatus: Optional[CodeableConcept] = None
    multipleBirthBoolean: Optional[bool] = None
    multipleBirthInteger: Optional[int] = None
    photo: Optional[List[Attachment]] = None
    contact: Optional[List[PatientResource.Contact]] = None
    communication: Optional[List[PatientResource.Communication]] = None
    generalPractitioner: Optional[List[Reference]] = None
    managingOrganization: Optional[Reference] = None
    link: Optional[List[PatientResource.Link]] = None

class PatientResponse(BaseModel):
    resourceType: str = "Patient"
    id: str
    identifier: List[Identifier] = Field(default_factory=list)
    active: Optional[bool] = None
    name: List[HumanName] = Field(default_factory=list)
    telecom: List[ContactPoint] = Field(default_factory=list)
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[str] = None
    address: List[Address] = Field(default_factory=list)
    maritalStatus: Optional[CodeableConcept] = None
    multipleBirthBoolean: Optional[bool] = None
    multipleBirthInteger: Optional[int] = None
    photo: List[Attachment] = Field(default_factory=list)
    contact: List[PatientResource.Contact] = Field(default_factory=list)
    communication: List[PatientResource.Communication] = Field(default_factory=list)
    generalPractitioner: List[Reference] = Field(default_factory=list)
    managingOrganization: Optional[Reference] = None
    link: List[PatientResource.Link] = Field(default_factory=list)

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
