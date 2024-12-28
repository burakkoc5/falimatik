from pydantic import BaseModel

class EmailVerificationRequest(BaseModel):
    token: str

class EmailVerificationResponse(BaseModel):
    message: str 