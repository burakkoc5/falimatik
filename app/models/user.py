from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from datetime import datetime, date
from app.database import Base
from passlib.context import CryptContext
from sqlalchemy.schema import UniqueConstraint
from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"
    
    # Add unique constraints explicitly
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        UniqueConstraint('username', name='uq_user_username'),
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    horoscope = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, unique=True, nullable=True)

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def calculate_horoscope(self) -> str:
        month = self.birthdate.month
        day = self.birthdate.day
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        else:
            return "Pisces"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.birthdate:
            self.horoscope = self.calculate_horoscope()

# Pydantic Models for API
class UserBase(BaseModel):
    """Base user schema with common attributes"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8)
    name: str
    birthdate: date
    gender: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "strongpassword123",
                "name": "John Doe",
                "birthdate": "1990-01-01",
                "gender": "male"
            }
        }
    )

class UserSignIn(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="Email for login")
    password: str = Field(..., description="User password")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }
    )

class UserInDB(UserBase):
    """Schema for user as stored in database"""
    id: int
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserBase):
    """Schema for user responses"""
    id: int
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for user updates"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)

    class Config:
        from_attributes = True
