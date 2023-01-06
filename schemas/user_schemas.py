from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import enum


class UserBase(BaseModel):
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr = "j_doe@gmail.com"
    password: str = "die_hard"


class RequestPassword(BaseModel):
    email: EmailStr = "j_doe@gmail.com"


class PasswordReset(BaseModel):
    new_password: str


class UserDisplay(BaseModel):
    id: int
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr = "j_doe@gmail.com"
    created_at: datetime
    last_update: Union[datetime, None]
    activated: bool
    verified: bool

