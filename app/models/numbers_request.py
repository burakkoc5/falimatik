from pydantic import BaseModel
from datetime import date as date_type

class DailyNumbersRequest(BaseModel):
    date: date_type

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-03-20"
            }
        }

class LuckyNumberRequest(BaseModel):
    date: date_type
    birthdate: date_type
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-03-20",
                "birthdate": "1990-01-01",
                "user_id": 1
            }
        } 