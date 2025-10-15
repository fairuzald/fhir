from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

class UserRole(str, Enum):
    ADMIN = "admin"
    CLINICIAN = "clinician"
    READ_ONLY = "read_only"

@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class Role:
    name: str
    permissions: list[str]
