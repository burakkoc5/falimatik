from pydantic import BaseModel, EmailStr
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    name: str
    birthdate: str
    gender: Gender = Gender.NOT_SPECIFIED  # Default value if not provided

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 