# app/services.py
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .dto import UserCreateDTO
from .repository import UserRepository
from .utils import PasswordUtil, JWTUtil
from .schemas import UserResponse
from .config import settings

class UserService:
    @staticmethod
    def register_user(db: Session, dto: UserCreateDTO):
        email = dto.email
        password = dto.password
        username = dto.username
        display_name = dto.display_name

        # 1) hash password
        password_hash = PasswordUtil.hash(password)

        # 2) create user in DB
        user = UserRepository.create_user(db, email=email, password_hash=password_hash, username=username, display_name=display_name)

        # 3) create token (subject = user.id)
        token_payload = {"sub": str(user.id), "email": user.email}
        token = JWTUtil.encode(token_payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        # 4) prepare response
        user_resp = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            display_name=user.display_name,
            email_verified=user.email_verified
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user_resp,
        }