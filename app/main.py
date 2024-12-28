from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.routes import auth_routes, horoscope_routes, numbers_routes
from fastapi.responses import JSONResponse
from app.models.response_models import ResponseModel
from app.models.auth import UserSignIn, Token
from app.models.user import UserCreate, User

# Load environment variables from .env file
load_dotenv()

# Test print to verify environment variables are loaded
print("Mail settings:", {
    "username": os.getenv("MAIL_USERNAME"),
    "server": os.getenv("MAIL_SERVER"),
    "port": os.getenv("MAIL_PORT")
})

app = FastAPI(
    title="Falimatik API",
    description="A FastAPI-based horoscope and lucky numbers API",
    version="1.0.0",
    openapi_tags=[
        {"name": "authentication", "description": "Authentication operations"},
        {"name": "horoscope", "description": "Horoscope operations"},
        {"name": "numbers", "description": "Lucky numbers operations"}
    ]
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Update the security scheme definition and add schemas
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token in the format: **Bearer <token>**"
            }
        },
        "schemas": {
            "ResponseModel": {
                "title": "ResponseModel",
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"},
                    "data": {"type": "object"}
                }
            },
            "UserSignIn": {
                "title": "UserSignIn",
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string"}
                },
                "required": ["email", "password"],
                "example": {
                    "email": "user@example.com",
                    "password": "secretpassword",
                }
            },
            "UserSignUp": {
                "title": "UserSignUp",
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "name": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"},
                    "gender": {"type": "string", "enum": ["male", "female", "other"]}
                },
                "required": ["email", "username", "password", "name", "birthdate", "gender"],
                "example": {
                    "email": "user@example.com",
                    "username": "johndoe",
                    "password": "secretpassword",
                    "name": "John Doe",
                    "birthdate": "1990-01-01",
                    "gender": "male"
                }
            },
            "Token": {
                "title": "Token",
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "token_type": {"type": "string"}
                }
            },
            "User": {
                "title": "User",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"},
                    "username": {"type": "string"},
                    "name": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"},
                    "gender": {"type": "string"},
                    "horoscope": {"type": "string"},
                    "is_verified": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"}
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"}
                    }
                }
            }
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Add security exclusions for auth routes
    if "paths" in openapi_schema:
        for path, path_item in openapi_schema["paths"].items():
            if path.startswith("/auth"):
                for operation in path_item.values():
                    operation["security"] = []

    # Fix schema references
    if "paths" in openapi_schema:
        for path in openapi_schema["paths"].values():
            for method in path.values():
                if "requestBody" in method:
                    if "content" in method["requestBody"]:
                        if "application/json" in method["requestBody"]["content"]:
                            schema = method["requestBody"]["content"]["application/json"]["schema"]
                            if "$ref" in schema:
                                ref = schema["$ref"].split("/")[-1]
                                if ref in openapi_schema["components"]["schemas"]:
                                    method["requestBody"]["content"]["application/json"]["schema"] = (
                                        openapi_schema["components"]["schemas"][ref]
                                    )
                
                if "responses" in method:
                    for response in method["responses"].values():
                        if "content" in response:
                            if "application/json" in response["content"]:
                                schema = response["content"]["application/json"]["schema"]
                                if "$ref" in schema:
                                    ref = schema["$ref"].split("/")[-1]
                                    if ref in openapi_schema["components"]["schemas"]:
                                        response["content"]["application/json"]["schema"] = (
                                            openapi_schema["components"]["schemas"][ref]
                                        )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(horoscope_routes.router)
app.include_router(numbers_routes.router)

@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ResponseModel(
            code=401,
            message="Authentication required. Please sign in first.",
            data=None
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            code=exc.status_code,
            message=exc.detail,
            data=None
        ).dict()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseModel(
            code=500,
            message="Internal server error",
            data=None
        ).dict()
    ) 