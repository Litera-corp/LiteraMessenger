# app/services.py
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .dto import UserCreateDTO
from .repository import UserRepository
from .utils import PasswordService, JWTTokenService
from .schemas import UserResponse
from .config import settings

class UserService:
    @staticmethod
    def register_user(db: Session, dto: UserCreateDTO):
        email = dto.email
        password = dto.password
        username = dto.username
        display_name = dto.display_name
        # 1) check email and username uniqueness
        existing_user_by_email = UserRepository.get_by_email(db, email)
        if existing_user_by_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже используется")
        existing_user_by_username = UserRepository.get_by_username(db, username)
        if existing_user_by_username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username уже используется")

        # 2) password validation
        match PasswordService.validate(password):
            case 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                    detail="Пароль должен содержать минимум 8 символов")
            case 2:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                    detail="Пароль должен содержать хотя бы 1 букву")
            case 3:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                    detail="Пароль должен содержать хотя бы 1 цифру")
            case 4:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                    detail="Пароль должен содержать хотя бы 1 спецсимвол")

        # 3) hash password
        password_hash = PasswordService.hash(password)

        # 4) create user in DB
        user = UserRepository.create_user(db, email=email, password_hash=password_hash, username=username, display_name=display_name)

        # 5) create token (subject = user.id)
        token_payload = {"sub": str(user.id), "email": user.email}
        token = JWTTokenService.encode(token_payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        # 6) prepare response
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