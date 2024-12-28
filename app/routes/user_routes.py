from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User, UserCreate
from app.services.user_service import UserService
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

# Add this class for update requests
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    horoscope: Optional[str] = None

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    user_service = UserService(db)
    return await user_service.create_user(user)

@router.get("/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve user information by their unique ID",
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/",
    response_model=List[User],
    summary="Get all users",
    description="Retrieve a list of all registered users"
)
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    user_service = UserService(db)
    return await user_service.get_all_users()

@router.put("/{user_id}",
    response_model=User,
    summary="Update user",
    description="""
    Update user information by their ID. You can update any of these fields:
    - username: New username
    - email: New email address
    - password: New password
    - birthdate: New birthdate (YYYY-MM-DD)
    - gender: New gender
    - horoscope: New horoscope sign
    """,
    responses={
        200: {
            "description": "User successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "username": "newusername",
                        "email": "newemail@example.com",
                        "birthdate": "1990-01-31",
                        "gender": "male",
                        "horoscope": "aquarius"
                    }
                }
            }
        },
        404: {"description": "User not found"},
        400: {"description": "Invalid input data"}
    }
)
async def update_user(
    user_id: int, 
    update_data: UserUpdate, 
    db: Session = Depends(get_db)
):
    """Update user information"""
    user_service = UserService(db)
    user = await user_service.update_user(user_id, update_data.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}",
    summary="Delete user",
    description="Delete a user by their ID",
    responses={
        204: {"description": "User successfully deleted"},
        404: {"description": "User not found"}
    }
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    user_service = UserService(db)
    if not await user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User deleted"} 