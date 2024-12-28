from fastapi import APIRouter, HTTPException
from app.services.horoscope_service import HoroscopeService
from app.models.horoscope_model import HoroscopeModel

router = APIRouter(prefix="/horoscope", tags=["horoscope"])

@router.get("/{sign}",
    response_model=HoroscopeModel,
    summary="Get daily horoscope",
    description="Get the daily horoscope message for a specific zodiac sign",
    responses={
        200: {
            "description": "Horoscope retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "date": "2024-03-19",
                        "sign": "leo",
                        "message": "Your creative energy is high. Show your talents!"
                    }
                }
            }
        },
        400: {
            "description": "Invalid zodiac sign",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid zodiac sign"}
                }
            }
        }
    }
)
async def get_horoscope(sign: str):
    """Get horoscope for a specific zodiac sign"""
    horoscope_service = HoroscopeService()
    try:
        return await horoscope_service.get_horoscope(sign)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 