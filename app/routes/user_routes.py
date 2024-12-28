from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User, UserCreate
from app.models.response_models import ResponseModel
from app.services.user_service import UserService
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.email_verification import EmailVerificationRequest, EmailVerificationResponse
from app.services.auth_service import AuthService
from app.utils.email import send_verification_email

router = APIRouter(prefix="/users", tags=["users"])

# Add this class for update requests
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    horoscope: Optional[str] = None

@router.post("/", response_model=ResponseModel[User])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    user_service = UserService(db)
    new_user = await user_service.create_user(user)
    
    # Generate and send verification token
    token = new_user.generate_verification_token()
    await send_verification_email(new_user.email, token)
    
    return ResponseModel.success(
        message="User created successfully",
        data=new_user
    )

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
    update_data: UserUpdate, 
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

@router.post("/verify/{token}", response_model=ResponseModel)
def verify_email(token: str, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    if auth_service.verify_email(token):
        return ResponseModel.success("Email verified successfully")
    return ResponseModel.error(400, "Email verification failed")

@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    if user_service.verify_user_email(token):
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired verification token") 