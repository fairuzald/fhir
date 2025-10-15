from typing import List
from .entities import User, UserRole

class AuthPolicies:
    """Authorization policies for different user roles"""

    @staticmethod
    def can_create_patient(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.CLINICIAN]

    @staticmethod
    def can_create_encounter(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.CLINICIAN]

    @staticmethod
    def can_create_observation(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.CLINICIAN]

    @staticmethod
    def can_read_all_resources(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.CLINICIAN, UserRole.READ_ONLY]

    @staticmethod
    def can_modify_resources(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.CLINICIAN]

    @staticmethod
    def can_delete_resources(user: User) -> bool:
        return user.role == UserRole.ADMIN

