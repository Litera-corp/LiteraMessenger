# app/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .repository import UserRepository
from .services import PasswordUtil
from .database import SessionLocal

class RegisterValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        body_bytes = await request.body()
        if not body_bytes:
            return JSONResponse({"detail": "Empty body"}, status_code=400)

        try:
            data = await request.json()
        except Exception:
            return JSONResponse({"detail": "Invalid JSON"}, status_code=400)

        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if not email or not username or not password:
            return JSONResponse({"detail": "Email, username, and password are required"}, status_code=422)

        # --- создаём сессию для проверки уникальности ---
        db: Session = SessionLocal()
        try:
            if UserRepository.get_by_email(db, email):
                return JSONResponse({"detail": "Email уже используется"}, status_code=409)
            if UserRepository.get_by_username(db, username):
                return JSONResponse({"detail": "Username уже используется"}, status_code=409)
        finally:
            db.close()

        # --- валидация пароля ---
        match PasswordUtil.validate(password):
            case 1:
                return JSONResponse({"detail": "The password must contain at least 8 characters."}, status_code=422)
            case 2:
                return JSONResponse({"detail": "The password must contain at least one letter."}, status_code=422)
            case 3:
                return JSONResponse({"detail": "The password must contain at least one digit"}, status_code=422)
            case 4:
                return JSONResponse({"detail": "The password must contain at least one special character"},
                                    status_code=422)
            case _:
                pass  # валидно

        # Сохраняем валидированные данные для роутера
        request.state.validated_body = data

        # Воссоздаём тело запроса для downstream
        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        new_request = Request(request.scope, receive)
        return await call_next(new_request)
