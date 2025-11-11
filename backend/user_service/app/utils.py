# app/utils.py
import re
import secrets
import string
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt  # PyJWT

from passlib.context import CryptContext
from .config import settings

# создаём контекст для bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Пароли ----------
def hash_password(password: str) -> str:
    """Принимает пароль в открытом виде и возвращает его безопасный хеш."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли открытый пароль хешу. Используется для логина."""
    return pwd_context.verify(plain_password, hashed_password)

# ---------- Токены (JWT) ----------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создаёт JWT access token.
    `data` - payload (например {"sub": user_id, "email": email})
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # PyJWT returns str on encode
    return encoded_jwt

# ---------- Верификационные коды ----------
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def is_valid_email(email: str) -> bool:
    """Простая проверка формата e-mail."""
    return bool(EMAIL_REGEX.match(email))

def generate_verification_code(length: int = 6) -> str:
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(length))

# ---------- Логгер ----------
logger = logging.getLogger("user_service")
logger.setLevel(logging.INFO)