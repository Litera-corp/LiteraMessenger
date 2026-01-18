# app/routes.py
from fastapi import APIRouter, Depends, Request, Body
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

from .services import UserService
from .dto import UserCreateDTO, UserLoginDTO
from .schemas import AuthResponse
from .database import get_db
from .validators import validate_register, validate_login

register_router = APIRouter()
login_router = APIRouter()


@register_router.post("/register", response_model=AuthResponse, status_code=201)
async def register_endpoint(
    db: Session = Depends(get_db),
    validated: UserCreateDTO = Depends(validate_register)
):
    # DTO уже валидирован через validate_register
    result = await run_in_threadpool(UserService.register_user, db, validated)
    return result


@login_router.post("/login", response_model=AuthResponse)
async def login_endpoint(
    request: Request = None,
    db: Session = Depends(get_db),
    validated: UserLoginDTO = Depends(validate_login)
):
    validated.ip_address = getattr(request.client, "host", None)
    validated.user_agent = request.headers.get("user-agent")
    result = await run_in_threadpool(UserService.auth_user, db, validated)
    return result
