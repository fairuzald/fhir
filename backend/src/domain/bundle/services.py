from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config.settings import settings


class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

class JWTService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: Dict[str, Any], expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ValueError("Invalid token")

class FHIRValidationService:
    """Service for FHIR resource validation"""

    @staticmethod
    def validate_patient_resource(resource: Dict[str, Any]) -> bool:
        """Validate Patient resource structure"""
        required_fields = ["resourceType"]
        for field in required_fields:
            if field not in resource:
                return False

        if resource["resourceType"] != "Patient":
            return False

        return True

    @staticmethod
    def validate_encounter_resource(resource: Dict[str, Any]) -> bool:
        """Validate Encounter resource structure"""
        required_fields = ["resourceType"]
        for field in required_fields:
            if field not in resource:
                return False

        if resource["resourceType"] != "Encounter":
            return False

        return True

    @staticmethod
    def validate_observation_resource(resource: Dict[str, Any]) -> bool:
        """Validate Observation resource structure"""
        required_fields = ["resourceType"]
        for field in required_fields:
            if field not in resource:
                return False

        if resource["resourceType"] != "Observation":
            return False

        return True
