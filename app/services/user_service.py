from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserDB, User
from typing import List
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def check_username_exists(self, username: str) -> bool:
        query = select(UserDB).where(UserDB.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

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