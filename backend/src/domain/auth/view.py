from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MeResponse(BaseModel):
    id: UUID
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

