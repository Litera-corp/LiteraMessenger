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

# ---------- Пароли ----------
class PasswordService:
    """
    Сервис для работы с паролями: хеширование, проверка, валидация.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        """Хеширует пароль."""
        return cls.pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль по хешу."""
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def validate(password: str) -> int:
        """
        Проверяет пароль и возвращает код:
        0 — валиден
        1 — слишком короткий
        2 — нет буквы
        3 — нет цифры
        4 — нет спецсимвола
        """
        if len(password) < 8:
            return 1
        if not re.search(r"[a-zA-Z]", password):
            return 2
        if not re.search(r"\d", password):
            return 3
        if not re.search(r"[!@#$%^&*()\-_=+[\]{};:,<.>/?]", password):
            return 4
        return 0

# ---------- Токены (JWT) ----------
class JWTTokenService:
    """
    Сервис для создания и проверки JWT токенов.
    """
    secret_key: str = settings.SECRET_KEY
    algorithm: str = settings.ALGORITHM
    default_exp_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def encode(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Создаёт JWT токен.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=cls.default_exp_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.secret_key, algorithm=cls.algorithm)

    @classmethod
    def decode(cls, token: str) -> dict:
        """
        Декодирует JWT токен.
        Выбрасывает исключения PyJWT при ошибке.
        """
        return jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])

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