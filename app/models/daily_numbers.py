from datetime import date
from pydantic import BaseModel
from typing import List

class DailyNumbers(BaseModel):
    date: date
    power_number: str  # 6-digit power number
    love_number: str   # 6-digit personal number
    career_number: str # 6-digit personal number
    health_number: str # 6-digit personal number
    finance_number: str # 6-digit personal number

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-03-19",
                "power_number": "123456",
                "love_number": "789012",
                "career_number": "345678",
                "health_number": "901234",
                "finance_number": "567890"
            }
        }
