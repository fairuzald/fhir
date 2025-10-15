from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.domain.auth.controller import AuthController
from src.domain.bundle.services import JWTService, PasswordService
from src.domain.fhir.patient.controller import PatientController
from src.infrastructure.db.base import Base
from src.infrastructure.db.repositories.auth_repo_sqlalchemy import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.db.repositories.fhir.patient_repo_sqlalchemy import (
    SQLAlchemyPatientRepository,
)
from src.infrastructure.db.session import engine

from .deps import get_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FHIR Simulation Server",
    description="A lightweight FHIR R4 server with authentication",
    version="1.0.0"
)

# Global error handlers to return FHIR OperationOutcome
@app.exception_handler(ValueError)
def handle_value_error(_: Request, exc: ValueError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "not-found", "diagnostics": str(exc)}]
    })

@app.exception_handler(PermissionError)
def handle_permission_error(_: Request, exc: PermissionError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "forbidden", "diagnostics": str(exc)}]
    })

@app.exception_handler(Exception)
def handle_unexpected_error(_: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "exception", "diagnostics": str(exc)}]
    })

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = SQLAlchemyUserRepository(db)
    password_service = PasswordService()
    jwt_service = JWTService()
    return AuthController(user_repo, password_service, jwt_service)

def get_patient_controller(db: Session = Depends(get_db)) -> PatientController:
    patient_repo = SQLAlchemyPatientRepository(db)
    return PatientController(patient_repo)

# Include routers
from .routes import router as api_router

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
