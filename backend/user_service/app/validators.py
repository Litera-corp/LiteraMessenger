# app/validators.py
from fastapi import HTTPException, status
from .utils import PasswordUtil, is_valid_email
from .repository import UserRepository
from .database import SessionLocal
from .dto import UserCreateDTO, UserLoginDTO

def validate_register(dto: UserCreateDTO) -> UserCreateDTO:
    email = dto.email
    username = dto.username
    password = dto.password

    # Проверка email
    if not is_valid_email(email):
        raise HTTPException(status_code=422, detail="Invalid email format")

    # Проверка уникальности
    db = SessionLocal()
    try:
        if UserRepository.get_by_email(db, email):
            raise HTTPException(status_code=409, detail="Email is already in use")
        if UserRepository.get_by_username(db, username):
            raise HTTPException(status_code=409, detail="Username is already in use")
    finally:
        db.close()

    # Проверка пароля
    match PasswordUtil.validate(password):
        case 1:
            raise HTTPException(status_code=422, detail="Password must be at least 8 characters long")
        case 2:
            raise HTTPException(status_code=422, detail="Password must contain at least one letter")
        case 3:
            raise HTTPException(status_code=422, detail="Password must contain at least one digit")
        case 4:
            raise HTTPException(status_code=422, detail="Password must contain at least one special character")

    return dto


def validate_login(dto: UserLoginDTO) -> UserLoginDTO:
    if not dto.identifier or not dto.password:
        raise HTTPException(status_code=422, detail="Identifier and password are required")
    return dto
