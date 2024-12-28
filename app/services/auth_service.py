from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserDB, UserSignUp, User
from app.models.auth import Token, UserSignIn
from fastapi import HTTPException
from datetime import datetime, timedelta
import secrets
from app.utils.email import send_verification_email
import jwt
import os

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    async def check_email_exists(self, email: str) -> bool:
        query = select(UserDB).where(UserDB.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def check_username_exists(self, username: str) -> bool:
        query = select(UserDB).where(UserDB.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def signup(self, user_data: UserSignUp) -> User:
        # Check if user exists
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
        try:
            await send_verification_email(user.email, token)
            print(f"Verification email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
        
        return User.from_orm(user)

    async def verify_email(self, token: str) -> bool:
        print(token)
        query = select(UserDB).where(UserDB.verification_token == token)
        print(query)
        result = await self.db.execute(query)
        print(result)
        user = result.scalar_one_or_none()
        print(user)

        if not user:
            return False
            
        user.is_verified = True
        user.verification_token = None
        await self.db.commit()
        return True 

    async def resend_verification_email(self, email: str) -> bool:
        # Find user by email
        query = select(UserDB).where(UserDB.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="No account found with this email address"
            )
            
        if user.is_verified:
            raise HTTPException(
                status_code=400,
                detail="This email is already verified"
            )
        
        # Generate new verification token
        token = secrets.token_urlsafe(32)
        user.verification_token = token
        
        await self.db.commit()
        
        # Send new verification email
        await send_verification_email(user.email, token)
        
        return True 

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def signin(self, credentials: UserSignIn) -> Token:
        # Find user by email
        query = select(UserDB).where(UserDB.email == credentials.email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=200,
                detail="Incorrect email or password"
            )

        # Verify password
        if not user.verify_password(credentials.password):
            raise HTTPException(
                status_code=200,
                detail="Incorrect email or password"
            )

        # Check if email is verified
        if not user.is_verified:
            raise HTTPException(
                status_code=200,
                detail="Please verify your email before signing in"
            )

        # Create access token
        access_token = self.create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )

        return Token(
            access_token=access_token,
            token_type="bearer"
        ) 