from datetime import date
from typing import Optional
from pydantic import BaseModel


class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    horoscope: Optional[str] = None