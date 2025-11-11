# app/services.py
from datetime import timedelta
from fastapi import HTTPException, status

from .repository import get_user_by_email, create_user
from .utils import hash_password, create_access_token
from .schemas import UserResponse
from .config import settings

def register_user(db, email: str, password: str, username: str = None, display_name: str = None):
    # 1) check email uniqueness
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже используется")

    # 2) hash password
    password_hash = hash_password(password)

    # 3) create user in DB
    user = create_user(db, email=email, password_hash=password_hash, username=username, display_name=display_name)

    # 4) create token (subject = user.id)
    token_payload = {"sub": str(user.id), "email": user.email}
    token = create_access_token(token_payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    # 5) prepare response
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