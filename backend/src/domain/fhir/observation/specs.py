from typing import List, Optional
from uuid import UUID
from .entities import Observation

class ObservationSpecs:
    """Business rules and specifications for Observation domain"""

    @staticmethod
    def is_valid_status(status: str) -> bool:
        """Validate observation status"""
        valid_statuses = [
            "registered", "preliminary", "final", "amended",
            "corrected", "cancelled", "entered-in-error", "unknown"
        ]
        return status in valid_statuses

    @staticmethod
    def is_valid_code(code: str) -> bool:
        """Validate observation code"""
        # Common LOINC codes for observations
        common_codes = [
            "8310-5",  # Body temperature
            "29463-7", # Body weight
            "8302-2",  # Body height
            "8867-4",  # Heart rate
            "9279-1",  # Respiratory rate
            "8480-6",  # Systolic blood pressure
            "8462-4"   # Diastolic blood pressure
        ]
        return code in common_codes

    @staticmethod
    def is_valid_value(value: float, unit: str) -> bool:
        """Validate observation value"""
        if unit == "°F" and (value < 90 or value > 110):
            return False
        if unit == "kg" and (value < 0 or value > 500):
            return False
        if unit == "cm" and (value < 0 or value > 300):
            return False
        return True

    @staticmethod
    def can_modify_observation(user_role: str) -> bool:
        """Check if user can modify observation data"""
        return user_role in ["admin", "clinician"]

    @staticmethod
    def can_delete_observation(user_role: str) -> bool:
        """Check if user can delete observation"""
        return user_role == "admin"

