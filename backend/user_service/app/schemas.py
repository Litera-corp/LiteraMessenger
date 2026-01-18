# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: Optional[str] = None
    display_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    display_name: Optional[str]
    email_verified: bool

    class Config:
        orm_mode = True

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse

class LoginRequest(BaseModel):
    """
    identifier: email OR username
    device_name: optional, например "iPhone 14 Pro" или "web:chrome"
    """
    identifier: str
    password: str
    device_name: Optional[str] = None