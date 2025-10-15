from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.infrastructure.db.session import get_db
from src.domain.auth.entities import User, UserRole
from src.domain.bundle.services import JWTService
from src.infrastructure.db.repositories.auth_repo_sqlalchemy import SQLAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    jwt_service = JWTService()
    try:
        payload = jwt_service.verify_token(token)
    except ValueError:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user

def require_role(required_role: UserRole):
    """Dependency to require specific role"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker
