from datetime import date
from pydantic import BaseModel

class HoroscopeModel(BaseModel):
    date: date
    sign: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-03-19",
                "sign": "leo",
                "message": "Today is a good day for new beginnings..."
            }
        }
