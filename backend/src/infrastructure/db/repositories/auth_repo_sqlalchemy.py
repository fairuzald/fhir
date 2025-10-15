from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.auth.entities import User, UserRole
from src.domain.auth.repositories import UserRepository
from src.infrastructure.db.models.auth import User as UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            role=UserRole(user_model.role),
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            role=UserRole(user_model.role),
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

    def create(self, user: User) -> User:
        user_model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,  # This should be set before calling
            role=user.role.value,
            is_active=user.is_active
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            role=UserRole(user_model.role),
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
