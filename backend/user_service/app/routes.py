# app/routes.py
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from .dto import UserCreateDTO
from .schemas import UserRegisterRequest, AuthResponse
from .services import UserService
from .database import get_db

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register_endpoint(user: UserRegisterRequest, db: Session = Depends(get_db)):
    dto = UserCreateDTO(**user.model_dump())
    # Если register_user синхронный, вызываем в threadpool
    result = await run_in_threadpool(
        UserService.register_user,
        db,
        dto
    )
    return result