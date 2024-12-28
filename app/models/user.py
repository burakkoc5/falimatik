from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import Base

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    horoscope = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    birthdate: date
    gender: str
    horoscope: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
