from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import UserCreate, UserSignIn, User
from app.models.token import Token
from app.models.response_models import ResponseModel
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post(
    "/signup", 
    response_model=ResponseModel,
    summary="User Sign Up",
    description="Register a new user with required information",
    responses={
        200: {
            "description": "Successful registration",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "user_id": 1,
                            "email": "user@example.com"
                        }
                    }
                }
            }
        }
    }
)
async def signup(
    user_data: UserCreate = Body(
        example={
            "email": "user@example.com",
            "username": "johndoe",
            "password": "strongpassword123",
            "name": "John Doe",
            "birthdate": "1990-01-01",
            "gender": "male"
        }
    ),
    db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        auth_service = AuthService(db)
        user = await auth_service.create_user(user_data)
        return ResponseModel(
            status="success",
            message="User registered successfully",
            data={"user_id": user.id, "email": user.email}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/signin",
    response_model=ResponseModel,
    summary="User Sign In",
    description="Sign in with email and password to get access token",
    responses={
        200: {
            "description": "Successful login",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "message": {"type": "string", "example": "Login successful"},
                            "data": {
                                "type": "object",
                                "properties": {
                                    "access_token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                                    "token_type": {"type": "string", "example": "bearer"}
                                }
                            }
                        }
                    },
                    "example": {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "token_type": "bearer"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string"}
                        }
                    },
                    "example": {
                        "detail": "Invalid credentials"
                    }
                }
            }
        }
    }
    
)
async def signin(
    credentials: UserSignIn = Body(
        example={
            "email": "user@example.com",
            "password": "strongpassword123"
        }
    ),
    db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    """
    Login with username and password
    
    - **username**: Your username
    - **password**: Your password
    """
    try:
        auth_service = AuthService(db)
        token = await auth_service.signin(credentials)
        return ResponseModel(
            status="success",
            message="Login successful",
            data={"access_token": token.access_token, "token_type": token.token_type}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/verify/{token}", response_model=ResponseModel)
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        auth_service = AuthService(db)
        await auth_service.verify_email(token)
        return ResponseModel(
            status="success",
            message="Email verified successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 