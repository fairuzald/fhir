from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.domain.auth.controller import AuthController
from src.domain.auth.entities import User, UserRole
from src.domain.auth.view import LoginRequest, MeResponse, TokenResponse
from src.domain.bundle.services import JWTService, PasswordService
from src.domain.fhir.encounter.controller import EncounterController
from src.domain.fhir.encounter.view import Bundle as EncounterBundle
from src.domain.fhir.encounter.view import (
    EncounterCreateRequest,
    EncounterResponse,
    EncounterSearchRequest,
)
from src.domain.fhir.observation.controller import ObservationController
from src.domain.fhir.observation.view import Bundle as ObservationBundle
from src.domain.fhir.observation.view import (
    ObservationCreateRequest,
    ObservationResponse,
    ObservationSearchRequest,
)
from src.domain.fhir.patient.controller import PatientController
from src.domain.fhir.patient.view import Bundle as PatientBundle
from src.domain.fhir.patient.view import (
    PatientCreateRequest,
    PatientResponse,
    PatientSearchRequest,
)
from src.infrastructure.db.repositories.auth_repo_sqlalchemy import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.db.repositories.fhir.encounter_repo_sqlalchemy import (
    SQLAlchemyEncounterRepository,
)
from src.infrastructure.db.repositories.fhir.observation_repo_sqlalchemy import (
    SQLAlchemyObservationRepository,
)
from src.infrastructure.db.repositories.fhir.patient_repo_sqlalchemy import (
    SQLAlchemyPatientRepository,
)
from src.interfaces.api.deps import get_current_user, get_db, require_role

router = APIRouter()

# Health check
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Auth endpoints
@router.post("/auth/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login endpoint"""
    user_repo = SQLAlchemyUserRepository(db)
    password_service = PasswordService()
    jwt_service = JWTService()
    auth_controller = AuthController(user_repo, password_service, jwt_service)

    try:
        return auth_controller.login(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/auth/me", response_model=MeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role.value,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

# FHIR endpoints
@router.get("/fhir/metadata")
def get_metadata():
    """FHIR CapabilityStatement endpoint"""
    from datetime import datetime
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": datetime.now().isoformat(),
        "publisher": "FHIR Simulation Server",
        "description": "A lightweight FHIR R4 server for simulation purposes",
        "fhirVersion": "4.0.1",
        "kind": "instance",
        "software": {"name": "FHIR Simulation Server", "version": "1.0.0"},
        "implementation": {"url": "http://localhost:8000/api/fhir"},
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "read"},
                            {"code": "vread"},
                            {"code": "update"},
                            {"code": "patch"},
                            {"code": "delete"},
                            {"code": "history-instance"},
                            {"code": "create"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "name", "type": "string"},
                            {"name": "identifier", "type": "token"}
                        ]
                    },
                    {
                        "type": "Encounter",
                        "interaction": [
                            {"code": "read"},
                            {"code": "vread"},
                            {"code": "update"},
                            {"code": "patch"},
                            {"code": "delete"},
                            {"code": "history-instance"},
                            {"code": "create"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "status", "type": "token"},
                            {"name": "subject", "type": "reference"},
                            {"name": "date", "type": "date"}
                        ]
                    },
                    {
                        "type": "Observation",
                        "interaction": [
                            {"code": "read"},
                            {"code": "vread"},
                            {"code": "update"},
                            {"code": "patch"},
                            {"code": "delete"},
                            {"code": "history-instance"},
                            {"code": "create"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "code", "type": "token"},
                            {"name": "date", "type": "date"},
                            {"name": "subject", "type": "reference"}
                        ]
                    }
                ]
            }
        ]
    }

# Patient endpoints
@router.get("/fhir/Patient/{patient_id}", response_model=PatientResponse)
def get_patient(
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

    patient_repo = SQLAlchemyPatientRepository(db)
    patient_controller = PatientController(patient_repo)

    try:
        return patient_controller.get_patient(patient_uuid, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.post("/fhir/Patient", response_model=PatientResponse)
def create_patient(
    request: PatientCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new patient"""
    patient_repo = SQLAlchemyPatientRepository(db)
    patient_controller = PatientController(patient_repo)

    try:
        return patient_controller.create_patient(request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/fhir/Patient", response_model=PatientBundle)
def search_patients(
    name: Optional[str] = Query(None),
    identifier: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search patients"""
    patient_repo = SQLAlchemyPatientRepository(db)
    patient_controller = PatientController(patient_repo)

    search_request = PatientSearchRequest(name=name, identifier=identifier)

    try:
        return patient_controller.search_patients(search_request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

# Patient update
@router.put("/fhir/Patient/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: str,
    request: PatientCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        patient_uuid = UUID(patient_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient ID format")

    patient_repo = SQLAlchemyPatientRepository(db)
    patient_controller = PatientController(patient_repo)

    try:
        return patient_controller.update_patient(patient_uuid, request, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Patient delete
@router.delete("/fhir/Patient/{patient_id}")
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        patient_uuid = UUID(patient_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient ID format")

    patient_repo = SQLAlchemyPatientRepository(db)
    patient_controller = PatientController(patient_repo)

    try:
        ok = patient_controller.delete_patient(patient_uuid, current_user)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return {"deleted": True}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Encounter endpoints
@router.get("/fhir/Encounter/{encounter_id}", response_model=EncounterResponse)
def get_encounter(
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

    encounter_repo = SQLAlchemyEncounterRepository(db)
    encounter_controller = EncounterController(encounter_repo)

    try:
        return encounter_controller.get_encounter(encounter_uuid, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.post("/fhir/Encounter", response_model=EncounterResponse)
def create_encounter(
    request: EncounterCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new encounter"""
    encounter_repo = SQLAlchemyEncounterRepository(db)
    encounter_controller = EncounterController(encounter_repo)

    try:
        return encounter_controller.create_encounter(request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/fhir/Encounter", response_model=EncounterBundle)
def search_encounters(
    status: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search encounters"""
    encounter_repo = SQLAlchemyEncounterRepository(db)
    encounter_controller = EncounterController(encounter_repo)

    search_request = EncounterSearchRequest(status=status, subject=subject, date=date)

    try:
        return encounter_controller.search_encounters(search_request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

# Encounter update
@router.put("/fhir/Encounter/{encounter_id}", response_model=EncounterResponse)
def update_encounter(
    encounter_id: str,
    request: EncounterCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        encounter_uuid = UUID(encounter_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid encounter ID format")

    encounter_repo = SQLAlchemyEncounterRepository(db)
    encounter_controller = EncounterController(encounter_repo)

    try:
        return encounter_controller.update_encounter(encounter_uuid, request, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Encounter delete
@router.delete("/fhir/Encounter/{encounter_id}")
def delete_encounter(
    encounter_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        encounter_uuid = UUID(encounter_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid encounter ID format")

    encounter_repo = SQLAlchemyEncounterRepository(db)
    encounter_controller = EncounterController(encounter_repo)

    try:
        ok = encounter_controller.delete_encounter(encounter_uuid, current_user)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encounter not found")
        return {"deleted": True}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Observation endpoints
@router.get("/fhir/Observation/{observation_id}", response_model=ObservationResponse)
def get_observation(
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

    observation_repo = SQLAlchemyObservationRepository(db)
    observation_controller = ObservationController(observation_repo)

    try:
        return observation_controller.get_observation(observation_uuid, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.post("/fhir/Observation", response_model=ObservationResponse)
def create_observation(
    request: ObservationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CLINICIAN))
):
    """Create a new observation"""
    observation_repo = SQLAlchemyObservationRepository(db)
    observation_controller = ObservationController(observation_repo)

    try:
        return observation_controller.create_observation(request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/fhir/Observation", response_model=ObservationBundle)
def search_observations(
    code: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search observations"""
    observation_repo = SQLAlchemyObservationRepository(db)
    observation_controller = ObservationController(observation_repo)

    search_request = ObservationSearchRequest(code=code, date=date, subject=subject)

    try:
        return observation_controller.search_observations(search_request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

# Observation update
@router.put("/fhir/Observation/{observation_id}", response_model=ObservationResponse)
def update_observation(
    observation_id: str,
    request: ObservationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid observation ID format")

    observation_repo = SQLAlchemyObservationRepository(db)
    observation_controller = ObservationController(observation_repo)

    try:
        return observation_controller.update_observation(observation_uuid, request, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Observation delete
@router.delete("/fhir/Observation/{observation_id}")
def delete_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid observation ID format")

    observation_repo = SQLAlchemyObservationRepository(db)
    observation_controller = ObservationController(observation_repo)

    try:
        ok = observation_controller.delete_observation(observation_uuid, current_user)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Observation not found")
        return {"deleted": True}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


    search_request = PatientSearchRequest(name=name, identifier=identifier)

    try:
        return patient_controller.search_patients(search_request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


    search_request = PatientSearchRequest(name=name, identifier=identifier)

    try:
        return patient_controller.search_patients(search_request, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
