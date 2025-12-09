# main.py
from fastapi import FastAPI
from app.routes import register_router, login_router

app = FastAPI(title="My Messenger API")
app.include_router(register_router, prefix="/users")
app.include_router(login_router, prefix="/users")
