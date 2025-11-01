# app/routes.py
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from .schemas import UserRegisterRequest, UserResponse
from .services import register_user
from .database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_endpoint(user: UserRegisterRequest, db = Depends(get_db)):
    # run_in_threadpool чтобы синхронная функция не блокировала event loop
    return await run_in_threadpool(
        register_user,
        db,
        user.email,
        user.password,
        user.username,
        user.display_name
    )
