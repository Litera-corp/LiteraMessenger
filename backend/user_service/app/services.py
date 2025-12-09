# app/services.py
import uuid
import logging
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional

from .dto import UserCreateDTO, UserLoginDTO
from .repository import UserRepository
from .utils import PasswordUtil, JWTUtil, RefreshTokenUtil
from .schemas import UserResponse
from .config import settings
from .models import User

logger = logging.getLogger("user_service")
logger.setLevel(logging.INFO)

class UserService:

    REFRESH_TOKEN_GEN_ATTEMPTS = 5
    REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 30)

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

    @classmethod
    def _generate_unique_refresh_token(cls, db: Session) -> str:
        token = None
        for attempt in range(cls.REFRESH_TOKEN_GEN_ATTEMPTS):
            token = RefreshTokenUtil.generate()
            existing = UserRepository.get_session_by_refresh_token(db, token)
            if not existing:
                return token
            logger.warning("Refresh token collision (rare) on attempt %s", attempt + 1)
        return token

    @classmethod
    def auth_user(
            cls,
            db: Session,
            dto: "UserLoginDTO",
    ):
        identifier = dto.identifier
        device_name = dto.device_name
        password = dto.password

        # Загрузим пользователя по email или username
        user = UserRepository.get_by_email_or_username(db, identifier)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Проверка пароля
        if not PasswordUtil.verify(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # --- Далее генерация токенов и сессии, как было ---
        jti = str(uuid.uuid4())
        access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_payload = {"sub": str(user.id), "email": user.email, "jti": jti}
        access_token = JWTUtil.encode(access_payload, expires_delta=access_expires)

        refresh_token = cls._generate_unique_refresh_token(db)
        refresh_expires_at = RefreshTokenUtil.expires_at(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)

        if device_name:
            existing = UserRepository.get_session_by_user_and_device(db, user.id, device_name)
            if existing:
                UserRepository.update_session(
                    db,
                    existing,
                    refresh_token=refresh_token,
                    expires_at=refresh_expires_at,
                )
            else:
                UserRepository.create_session(
                    db,
                    user_id=user.id,
                    refresh_token=refresh_token,
                    device_name=device_name,
                    expires_at=refresh_expires_at,
                )
        else:
            UserRepository.create_session(
                db,
                user_id=user.id,
                refresh_token=refresh_token,
                device_name=None,
                expires_at=refresh_expires_at,
            )

        # Build response
        user_resp = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            display_name=user.display_name,
            email_verified=user.email_verified,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_resp,
        }
