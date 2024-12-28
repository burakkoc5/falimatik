from sqlalchemy.orm import Session
from app.models.user import UserDB, User, UserCreate
from app.database import get_db
from typing import List

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        db_user = UserDB(**user_data.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User.from_orm(db_user)

    async def get_user_by_id(self, user_id: int) -> User:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        return User.from_orm(db_user) if db_user else None

    async def get_all_users(self) -> List[User]:
        db_users = self.db.query(UserDB).all()
        return [User.from_orm(user) for user in db_users]

    async def update_user(self, user_id: int, update_data: dict) -> User:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return None
            
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