# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# создаём синхронный движок
engine = create_engine(DATABASE_URL, echo=False)

# создаём фабрику сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
