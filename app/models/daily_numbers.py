from datetime import date
from pydantic import BaseModel
from typing import List

class DailyNumbers(BaseModel):
    date: date
    power_number: int  # The daily number that's same for everyone
    love_number: int
    career_number: int
    health_number: int
    finance_number: int

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
