from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema for access token"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for token payload"""
    sub: Optional[str] = None  # user_id
    exp: Optional[int] = None  # expiration time 