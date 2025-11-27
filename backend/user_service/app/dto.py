# app/dto.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    display_name: Optional[str] = None

    model_config = ConfigDict(frozen=True)
