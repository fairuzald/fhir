from typing import List, Optional
from uuid import UUID
from .entities import Patient

class PatientSpecs:
    """Business rules and specifications for Patient domain"""

    @staticmethod
    def is_valid_identifier(identifier: str) -> bool:
        """Validate patient identifier format"""
        return len(identifier) >= 3 and identifier.isalnum()

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """Validate patient name"""
        return len(name.strip()) >= 2

    @staticmethod
    def is_valid_birth_date(birth_date) -> bool:
        """Validate birth date"""
        from datetime import date
        today = date.today()
        return birth_date <= today

    @staticmethod
    def can_modify_patient(user_role: str) -> bool:
        """Check if user can modify patient data"""
        return user_role in ["admin", "clinician"]

    @staticmethod
    def can_delete_patient(user_role: str) -> bool:
        """Check if user can delete patient"""
        return user_role == "admin"

