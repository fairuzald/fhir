from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.infrastructure.database import get_db
from app.infrastructure.database.models import Patient as PatientModel, Encounter as EncounterModel, Observation as ObservationModel
from app.application.auth_service import get_current_user, require_role
from app.domain.entities import User, UserRole
from app.domain.fhir_models import (
    PatientResource, EncounterResource, ObservationResource,
    Bundle, BundleEntry, OperationOutcome, OperationOutcomeIssue,
    CapabilityStatement
)
from app.config import settings

router = APIRouter()

# Metadata endpoint
@router.get("/metadata")
async def get_metadata():
    """FHIR CapabilityStatement endpoint"""
    return CapabilityStatement(date=datetime.now())

# Patient endpoints
@router.get("/Patient/{patient_id}")
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific patient by ID"""
    try:
        patient_uuid = UUID(patient_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient ID format"
        )

    patient = db.query(PatientModel).filter(PatientModel.id == patient_uuid).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return PatientResource(**patient.resource)

@router.post("/Patient")
async def create_patient(
    patient: PatientResource,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new patient"""
    # Extract searchable fields
    identifier_value = None
    name_family = None
    name_given = None

    if patient.identifier:
        identifier_value = patient.identifier[0].value if patient.identifier[0].value else None

    if patient.name:
        name_family = patient.name[0].family
        name_given = ", ".join(patient.name[0].given) if patient.name[0].given else None

    db_patient = PatientModel(
        identifier_value=identifier_value,
        name_family=name_family,
        name_given=name_given,
        gender=patient.gender,
        birth_date=patient.birthDate,
        resource=patient.dict()
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    # Update the resource with the generated ID
    patient.id = str(db_patient.id)
    db_patient.resource = patient.dict()
    db.commit()

    return PatientResource(**db_patient.resource)

@router.get("/Patient")
async def search_patients(
    name: Optional[str] = Query(None),
    identifier: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search patients"""
    query = db.query(PatientModel)

    if name:
        query = query.filter(
            (PatientModel.name_family.ilike(f"%{name}%")) |
            (PatientModel.name_given.ilike(f"%{name}%"))
        )

    if identifier:
        query = query.filter(PatientModel.identifier_value.ilike(f"%{identifier}%"))

    patients = query.all()

    entries = []
    for patient in patients:
        entries.append(BundleEntry(resource=PatientResource(**patient.resource)))

    return Bundle(
        total=len(entries),
        entry=entries
    )

# Encounter endpoints
@router.get("/Encounter/{encounter_id}")
async def get_encounter(
    encounter_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific encounter by ID"""
    try:
        encounter_uuid = UUID(encounter_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid encounter ID format"
        )

    encounter = db.query(EncounterModel).filter(EncounterModel.id == encounter_uuid).first()
    if not encounter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encounter not found"
        )

    return EncounterResource(**encounter.resource)

@router.post("/Encounter")
async def create_encounter(
    encounter: EncounterResource,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new encounter"""
    # Extract searchable fields
    subject_patient_id = None
    if encounter.subject and encounter.subject.reference:
        try:
            subject_patient_id = UUID(encounter.subject.reference.split("/")[-1])
        except (ValueError, IndexError):
            pass

    period_start = encounter.period.start if encounter.period else None
    period_end = encounter.period.end if encounter.period else None

    class_code = None
    if encounter.class_:
        class_code = encounter.class_.code

    reason_code = None
    if encounter.reasonCode and encounter.reasonCode[0].coding:
        reason_code = encounter.reasonCode[0].coding[0].code

    db_encounter = EncounterModel(
        status=encounter.status,
        class_code=class_code,
        subject_patient_id=subject_patient_id,
        period_start=period_start,
        period_end=period_end,
        reason_code=reason_code,
        resource=encounter.dict()
    )

    db.add(db_encounter)
    db.commit()
    db.refresh(db_encounter)

    # Update the resource with the generated ID
    encounter.id = str(db_encounter.id)
    db_encounter.resource = encounter.dict()
    db.commit()

    return EncounterResource(**db_encounter.resource)

@router.get("/Encounter")
async def search_encounters(
    status: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search encounters"""
    query = db.query(EncounterModel)

    if status:
        query = query.filter(EncounterModel.status == status)

    if subject:
        try:
            subject_uuid = UUID(subject.split("/")[-1])
            query = query.filter(EncounterModel.subject_patient_id == subject_uuid)
        except (ValueError, IndexError):
            pass

    if date:
        # Simple date filtering - could be enhanced
        query = query.filter(EncounterModel.period_start >= date)

    encounters = query.all()

    entries = []
    for encounter in encounters:
        entries.append(BundleEntry(resource=EncounterResource(**encounter.resource)))

    return Bundle(
        total=len(entries),
        entry=entries
    )

# Observation endpoints
@router.get("/Observation/{observation_id}")
async def get_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific observation by ID"""
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid observation ID format"
        )

    observation = db.query(ObservationModel).filter(ObservationModel.id == observation_uuid).first()
    if not observation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found"
        )

    return ObservationResource(**observation.resource)

@router.post("/Observation")
async def create_observation(
    observation: ObservationResource,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new observation"""
    # Extract searchable fields
    subject_patient_id = None
    if observation.subject and observation.subject.reference:
        try:
            subject_patient_id = UUID(observation.subject.reference.split("/")[-1])
        except (ValueError, IndexError):
            pass

    encounter_id = None
    if observation.encounter and observation.encounter.reference:
        try:
            encounter_id = UUID(observation.encounter.reference.split("/")[-1])
        except (ValueError, IndexError):
            pass

    code_code = None
    if observation.code and observation.code.coding:
        code_code = observation.code.coding[0].code

    value_quantity_value = None
    value_quantity_unit = None
    if observation.valueQuantity:
        value_quantity_value = observation.valueQuantity.value
        value_quantity_unit = observation.valueQuantity.unit

    db_observation = ObservationModel(
        status=observation.status,
        code_code=code_code,
        subject_patient_id=subject_patient_id,
        encounter_id=encounter_id,
        effective_datetime=observation.effectiveDateTime,
        value_quantity_value=value_quantity_value,
        value_quantity_unit=value_quantity_unit,
        value_string=observation.valueString,
        resource=observation.dict()
    )

    db.add(db_observation)
    db.commit()
    db.refresh(db_observation)

    # Update the resource with the generated ID
    observation.id = str(db_observation.id)
    db_observation.resource = observation.dict()
    db.commit()

    return ObservationResource(**db_observation.resource)

@router.get("/Observation")
async def search_observations(
    code: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search observations"""
    query = db.query(ObservationModel)

    if code:
        query = query.filter(ObservationModel.code_code == code)

    if subject:
        try:
            subject_uuid = UUID(subject.split("/")[-1])
            query = query.filter(ObservationModel.subject_patient_id == subject_uuid)
        except (ValueError, IndexError):
            pass

    if date:
        # Simple date filtering - could be enhanced
        query = query.filter(ObservationModel.effective_datetime >= date)

    observations = query.all()

    entries = []
    for observation in observations:
        entries.append(BundleEntry(resource=ObservationResource(**observation.resource)))

    return Bundle(
        total=len(entries),
        entry=entries
    )

# Bundle submission endpoint
@router.post("/$submit-bundle")
async def submit_bundle(
    bundle: Bundle,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Submit a bundle of resources"""
    if not bundle.entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bundle must contain entries"
        )

    results = []
    for entry in bundle.entry:
        if not entry.resource:
            continue

        resource = entry.resource

        if isinstance(resource, PatientResource):
            # Create patient
            db_patient = PatientModel(
                identifier_value=resource.identifier[0].value if resource.identifier else None,
                name_family=resource.name[0].family if resource.name else None,
                name_given=", ".join(resource.name[0].given) if resource.name and resource.name[0].given else None,
                gender=resource.gender,
                birth_date=resource.birthDate,
                resource=resource.dict()
            )
            db.add(db_patient)
            db.commit()
            db.refresh(db_patient)
            results.append({"resourceType": "Patient", "id": str(db_patient.id)})

        elif isinstance(resource, EncounterResource):
            # Create encounter
            subject_patient_id = None
            if resource.subject and resource.subject.reference:
                try:
                    subject_patient_id = UUID(resource.subject.reference.split("/")[-1])
                except (ValueError, IndexError):
                    pass

            db_encounter = EncounterModel(
                status=resource.status,
                class_code=resource.class_.code if resource.class_ else None,
                subject_patient_id=subject_patient_id,
                period_start=resource.period.start if resource.period else None,
                period_end=resource.period.end if resource.period else None,
                reason_code=resource.reasonCode[0].coding[0].code if resource.reasonCode and resource.reasonCode[0].coding else None,
                resource=resource.dict()
            )
            db.add(db_encounter)
            db.commit()
            db.refresh(db_encounter)
            results.append({"resourceType": "Encounter", "id": str(db_encounter.id)})

        elif isinstance(resource, ObservationResource):
            # Create observation
            subject_patient_id = None
            if resource.subject and resource.subject.reference:
                try:
                    subject_patient_id = UUID(resource.subject.reference.split("/")[-1])
                except (ValueError, IndexError):
                    pass

            encounter_id = None
            if resource.encounter and resource.encounter.reference:
                try:
                    encounter_id = UUID(resource.encounter.reference.split("/")[-1])
                except (ValueError, IndexError):
                    pass

            db_observation = ObservationModel(
                status=resource.status,
                code_code=resource.code.coding[0].code if resource.code and resource.code.coding else None,
                subject_patient_id=subject_patient_id,
                encounter_id=encounter_id,
                effective_datetime=resource.effectiveDateTime,
                value_quantity_value=resource.valueQuantity.value if resource.valueQuantity else None,
                value_quantity_unit=resource.valueQuantity.unit if resource.valueQuantity else None,
                value_string=resource.valueString,
                resource=resource.dict()
            )
            db.add(db_observation)
            db.commit()
            db.refresh(db_observation)
            results.append({"resourceType": "Observation", "id": str(db_observation.id)})

    return {"status": "success", "created": results}

