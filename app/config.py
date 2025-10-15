import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://fhir_user:fhir_password@localhost:5432/fhir_db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # FHIR
    FHIR_VERSION: str = "R4"
    FHIR_BASE_URL: str = os.getenv("FHIR_BASE_URL", "http://localhost:8000/fhir")

settings = Settings()

