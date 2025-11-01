# app/services.py
from fastapi import HTTPException, status
from .repository import get_user_by_email, create_user
from .utils import hash_password
from .schemas import UserResponse

def register_user(db, email: str, password: str, username: str = None, display_name: str = None) -> UserResponse:
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже используется")

    password_hash = hash_password(password)
    user = create_user(db, email, password_hash, username, display_name)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        email_verified=user.email_verified
    )
