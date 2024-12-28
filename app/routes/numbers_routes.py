from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.security.custom_bearer import CustomHTTPBearer
from app.services.numbers_service import NumbersService
from app.models.response_models import ResponseModel
from datetime import date

router = APIRouter(
    prefix="/numbers",
    tags=["numbers"],
    dependencies=[Depends(CustomHTTPBearer())]
)

@router.get("/lucky", response_model=ResponseModel)
async def get_lucky_numbers(birthdate: date, user_id: int, date: date, db: AsyncSession = Depends(get_db)):
    try:
        numbers_service = NumbersService(db)
        numbers = await numbers_service.calculate_lucky_numbers(birthdate, user_id, date)
        return ResponseModel.success(
            "Lucky numbers calculated successfully",
            {
                "date": numbers["date"].isoformat(),
                "love_number": numbers["love_number"],
                "career_number": numbers["career_number"],
                "health_number": numbers["health_number"],
                "finance_number": numbers["finance_number"]
            }
        )
    except HTTPException as e:
        return ResponseModel.error(e.status_code, e.detail)
    except Exception as e:
        return ResponseModel.error(500, str(e))

@router.get("/daily", response_model=ResponseModel)
async def get_daily_numbers(date: date, db: AsyncSession = Depends(get_db)):
    try:
        numbers_service = NumbersService(db)
        numbers = await numbers_service.get_daily_numbers(date)
        return ResponseModel.success(
            "Daily power number retrieved successfully",
            {
                "date": numbers["date"].isoformat(),
                "power_number": numbers["power_number"]
            }
        )
    except HTTPException as e:
        return ResponseModel.error(e.status_code, e.detail)
    except Exception as e:
        return ResponseModel.error(500, str(e)) 