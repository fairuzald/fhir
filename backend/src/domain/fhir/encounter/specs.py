from typing import List, Optional
from uuid import UUID
from .entities import Encounter

class EncounterSpecs:
    """Business rules and specifications for Encounter domain"""

    @staticmethod
    def is_valid_status(status: str) -> bool:
        """Validate encounter status"""
        valid_statuses = [
            "planned", "arrived", "triaged", "in-progress",
            "onleave", "finished", "cancelled", "entered-in-error", "unknown"
        ]
        return status in valid_statuses

    @staticmethod
    def is_valid_class_code(class_code: str) -> bool:
        """Validate encounter class code"""
        valid_codes = ["AMB", "EMER", "HH", "IMP", "ACUTE", "NONAC", "PRENC", "SS", "VR"]
        return class_code in valid_codes

    @staticmethod
    def is_valid_period(start: datetime, end: datetime) -> bool:
        """Validate encounter period"""
        if start and end:
            return start <= end
        return True

    @staticmethod
    def can_modify_encounter(user_role: str) -> bool:
        """Check if user can modify encounter data"""
        return user_role in ["admin", "clinician"]

    @staticmethod
    def can_delete_encounter(user_role: str) -> bool:
        """Check if user can delete encounter"""
        return user_role == "admin"

