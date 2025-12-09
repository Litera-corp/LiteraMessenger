# app/dto.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    display_name: Optional[str] = None

    model_config = ConfigDict(frozen=True)

class UserLoginDTO(BaseModel):
    identifier: str  # email или username
    password: str
    user_id: int     # кладётся middleware после проверки пароля
    device_name: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None