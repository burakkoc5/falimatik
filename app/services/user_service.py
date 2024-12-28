from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserDB, User, UserCreate
from app.database import get_db
from typing import List
from fastapi import HTTPException, status
from datetime import datetime
from app.services.email_service import EmailService
from app.utils.email import send_verification_email
import secrets

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()

    async def check_email_exists(self, email: str) -> bool:
        query = select(UserDB).where(UserDB.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def check_username_exists(self, username: str) -> bool:
        query = select(UserDB).where(UserDB.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def create_user(self, user_data: UserCreate) -> User:
        # Check if user already exists
        if await self.check_email_exists(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await self.check_username_exists(user_data.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        # Create user
        user = UserDB(**user_data.dict(exclude={'password'}))
        user.set_password(user_data.password)
        
        # Generate verification token
        token = secrets.token_urlsafe(32)
        user.verification_token = token
        user.is_verified = False
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        # Send verification email
        await send_verification_email(user.email, token)
        
        return User.from_orm(user)

    def verify_email(self, token: str) -> bool:
        user = self.db.query(UserDB).filter(
            UserDB.verification_token == token,
            UserDB.verification_token_expires > datetime.now()
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        
        self.db.commit()
        return True

    async def get_user_by_id(self, user_id: int) -> User:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        return User.from_orm(db_user) if db_user else None

    async def get_all_users(self) -> List[User]:
        db_users = self.db.query(UserDB).all()
        return [User.from_orm(user) for user in db_users]

    async def update_user(self, user_id: int, update_data: dict) -> User:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prevent email updates
        if 'email' in update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email cannot be changed after registration"
            )
        
        # Check username uniqueness if username is being updated
        if 'username' in update_data and update_data['username'] != db_user.username:
            if await self.check_username_exists(update_data['username']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        self.db.commit()
        self.db.refresh(db_user)
        return User.from_orm(db_user)

    async def delete_user(self, user_id: int) -> bool:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return False
            
        self.db.delete(db_user)
        self.db.commit()
        return True 