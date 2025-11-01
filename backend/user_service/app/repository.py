# app/repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password_hash: str, username: str = None, display_name: str = None):
    new_user = User(
        email=email,
        password_hash=password_hash,
        username=username,
        display_name=display_name
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(new_user)
    return new_user
