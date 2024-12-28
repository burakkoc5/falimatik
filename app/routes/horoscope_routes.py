from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.services.service_factory import get_horoscope_service
from app.models.response_models import ResponseModel
from app.models.user import User

router = APIRouter(
    prefix="/horoscope",
    tags=["horoscope"]
)

@router.get("/daily", response_model=ResponseModel)
async def get_daily_horoscope(
    sign: str,
    day: Optional[str] = "today"
    
) -> ResponseModel:
    """
    Get daily horoscope for a specific zodiac sign.
    """
    try:
        horoscope_service = get_horoscope_service()
        result = await horoscope_service.execute(sign=sign, day=day)
        print(result)
        return ResponseModel(
            status="success",
            message=f"Daily horoscope for {sign}",
            data=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get horoscope: {str(e)}"
        ) 