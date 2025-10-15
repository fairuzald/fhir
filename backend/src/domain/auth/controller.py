from uuid import UUID
from .repositories import UserRepository
from .view import LoginRequest, TokenResponse, MeResponse
from ..bundle.services import PasswordService, JWTService

class AuthController:
    def __init__(
        self,
        user_repo: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService
    ):
        self.user_repo = user_repo
        self.password_service = password_service
        self.jwt_service = jwt_service

    def login(self, request: LoginRequest) -> TokenResponse:
        """Handle user login"""
        user = self.user_repo.get_by_email(request.email)
        if not user:
            raise ValueError("Invalid credentials")

        if not self.password_service.verify_password(request.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User is inactive")

        token = self.jwt_service.create_access_token({"sub": user.email})
        return TokenResponse(access_token=token, token_type="bearer")

    def get_me(self, user_id: UUID) -> MeResponse:
        """Get current user profile"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return MeResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
