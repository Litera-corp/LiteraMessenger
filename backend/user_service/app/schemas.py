# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: Optional[str] = None
    display_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    display_name: Optional[str]
    email_verified: bool

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse