# app/models.py
from sqlalchemy import Column, BigInteger, String, Boolean, Text, TIMESTAMP, func, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=True)
    display_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    last_login_at = Column(TIMESTAMP, nullable=True)
    last_seen_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "users"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.users.id", ondelete="CASCADE"), nullable=False)
    device_name = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    refresh_token = Column(String(255), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="sessions", lazy="joined")


# Индексы для ускорения поиска по user_id и refresh_token (совпадает с твоим SQL)
Index("idx_sessions_user_id", UserSession.user_id)
Index("idx_sessions_refresh_token", UserSession.refresh_token)