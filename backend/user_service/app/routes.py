# app/routes.py
from fastapi import FastAPI, Request, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from .middleware import RegisterValidationMiddleware
from .dto import UserCreateDTO
from .schemas import UserRegisterRequest, AuthResponse
from .services import UserService
from .database import get_db

register_app = FastAPI()
register_app.add_middleware(RegisterValidationMiddleware)

@register_app.post("/register", response_model=AuthResponse, status_code=201)
async def register_endpoint(request: Request, db: Session = Depends(get_db)):
    # Берём данные из middleware
    data = getattr(request.state, "validated_body", None)
    if not data:
        data = await request.json()
    dto = UserCreateDTO(**data)
    result = await run_in_threadpool(UserService.register_user, db, dto)
    return result
