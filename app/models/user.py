from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from datetime import datetime, date, timedelta
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from app.database import Base
import bcrypt
import secrets
from sqlalchemy.schema import UniqueConstraint

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
    birthdate = Column(Date, nullable=False)
    horoscope = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, unique=True, nullable=True)

    def set_password(self, password: str):
        # Convert the password to bytes
        password_bytes = password.encode('utf-8')
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Store the hashed password as string
        self.password = hashed.decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        # Convert both passwords to bytes for comparison
        password_bytes = password.encode('utf-8')
        stored_password_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_password_bytes)

    def generate_verification_token(self) -> str:
        if not self.is_verified:
            self.verification_token = secrets.token_urlsafe(32)
            return self.verification_token
        return None

    def verify_email(self) -> bool:
        if not self.is_verified:
            self.is_verified = True
            self.verification_token = None
            return True
        return False
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

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    birthdate: date
    gender: str
    horoscope: Optional[str] = None
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
        })
    
class UserSignUp(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_verified: bool

    class Config:

        orm_mode = True
        from_attributes = True

