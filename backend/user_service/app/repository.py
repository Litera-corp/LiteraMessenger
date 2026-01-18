# app/repository.py
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import User, UserSession

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
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

    @staticmethod
    def get_by_email_or_username(db: Session, identifier: str) -> Optional[User]:
        """
        Ищет пользователя по email (если в идентификаторе есть '@'), иначе по username.
        Возвращает объект User или None.
        """
        if not identifier:
            return None
        user = None
        if "@" in identifier:
            user = db.query(User).filter(User.email == identifier).first()
        if not user:
            user = db.query(User).filter(User.username == identifier).first()
        return user

    @staticmethod
    def get_session_by_user_and_device(db: Session, user_id: int, device_name: Optional[str]) -> Optional[UserSession]:
        """
        Возвращает активную сессию для пары (user_id, device_name).
        Если device_name is None — вернёт None (чтобы не путать с множеством сессий без device_name).
        """
        if not device_name:
            return None
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.device_name == device_name,
            UserSession.is_active == True
        ).first()

    @staticmethod
    def get_session_by_refresh_token(db: Session, refresh_token: str) -> Optional[UserSession]:
        """
        Находит активную сессию по refresh_token.
        """
        if not refresh_token:
            return None
        return db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True
        ).first()

    @staticmethod
    def create_session(
            db: Session,
            user_id: int,
            refresh_token: str,
            device_name: Optional[str] = None,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None,
            expires_at: Optional[datetime] = None
    ) -> UserSession:
        """
        Создаёт новую запись сессии и возвращает её.
        """
        session = UserSession(
            user_id=user_id,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
            refresh_token=refresh_token,
            is_active=True,
            expires_at=expires_at
        )
        db.add(session)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(session)
        return session

    @staticmethod
    def update_session(
            db: Session,
            session: UserSession,
            refresh_token: Optional[str] = None,
            expires_at: Optional[datetime] = None,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None,
    ) -> UserSession:
        """
        Обновляет существующую сессию (замена refresh_token, expires_at, ip, user_agent).
        Также помечает is_active = True.
        """
        if refresh_token is not None:
            session.refresh_token = refresh_token
        if expires_at is not None:
            session.expires_at = expires_at
        if ip_address is not None:
            session.ip_address = ip_address
        if user_agent is not None:
            session.user_agent = user_agent

        session.is_active = True
        # обновим created_at/last поля не трогаем, в модели есть created_at автоустановка
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def deactivate_session(db: Session, session: UserSession) -> UserSession:
        """
        Дезактивирует сессию (logout).
        """
        session.is_active = False
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
