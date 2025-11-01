# app/utils.py
from passlib.context import CryptContext

# создаём контекст для bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Принимает пароль в открытом виде и возвращает его безопасный хеш.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли открытый пароль хешу.
    Используется для логина.
    """
    return pwd_context.verify(plain_password, hashed_password)
