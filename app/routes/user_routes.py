from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User, UserSignUp
from app.models.response_models import ResponseModel
from app.services.user_service import UserService
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel, EmailStr
from app.models.user_update_model import UserUpdateModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=ResponseModel[User])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        return ResponseModel.error(404, "User not found")
    return ResponseModel.success("User retrieved successfully", user)

@router.get("/", response_model=ResponseModel[List[User]])
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    user_service = UserService(db)
    users = await user_service.get_all_users()
    return ResponseModel.success("Users retrieved successfully", users)

@router.put("/{user_id}", response_model=ResponseModel[User])
async def update_user(
    user_id: int, 
    update_data: UserUpdateModel, 
    db: Session = Depends(get_db)
):
    """Update user information"""
    user_service = UserService(db)
    updated_user = await user_service.update_user(user_id, update_data.dict(exclude_unset=True))
    return ResponseModel.success("User updated successfully", updated_user)

@router.delete("/{user_id}", response_model=ResponseModel)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    user_service = UserService(db)
    if await user_service.delete_user(user_id):
        return ResponseModel.success("User deleted successfully")
    return ResponseModel.error(404, "User not found")
