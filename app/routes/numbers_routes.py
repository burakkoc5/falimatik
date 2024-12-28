from fastapi import APIRouter, HTTPException
from datetime import date
from app.services.numbers_service import NumbersService
from app.models.daily_numbers import DailyNumbers

router = APIRouter(prefix="/numbers", tags=["lucky numbers"])

@router.get("/power",
    summary="Get daily power number",
    description="Get the universal power number for the day (same for all users)",
    responses={
        200: {
            "description": "Power number retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "date": "2024-03-19",
                        "power_number": "123456"
                    }
                }
            }
        }
    }
)
async def get_power_number(target_date: date = None):
    """Get daily power number"""
    numbers_service = NumbersService()
    power_number = await numbers_service.get_power_number(target_date)
    return {
        "date": target_date or date.today(),
        "power_number": power_number
    }

@router.get("/personal/{user_id}",
    response_model=DailyNumbers,
    summary="Get personal daily numbers",
    description="""
    Get personalized lucky numbers based on user's birthdate.
    Generates 5 different 6-digit numbers:
    - Power number (universal daily number)
    - Love number (personal)
    - Career number (personal)
    - Health number (personal)
    - Finance number (personal)
    """,
    responses={
        200: {
            "description": "Personal numbers retrieved successfully"
        },
        404: {
            "description": "User not found"
        }
    }
)
async def get_personal_numbers(user_id: int, target_date: date = None):
    """Get personal daily numbers for a user"""
    from app.services.user_service import UserService  # Import here to avoid circular imports
    
    # Get user's birthdate
    user_service = UserService()
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate numbers
    numbers_service = NumbersService()
    return await numbers_service.get_personal_numbers(
        user_id=user_id,
        birthdate=user.birthdate,
        target_date=target_date
    ) 