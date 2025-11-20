from fastapi import FastAPI
from app.routes import register_app

app = FastAPI()

app.mount("/users", register_app)
