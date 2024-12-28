from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.requests import Request
from app.models.response_models import ResponseModel
from fastapi.responses import JSONResponse
import logging
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger(__name__)

class CustomHTTPBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        try:
            auth = request.headers.get("Authorization")
            print(auth)
            logger.debug(f"Received Authorization header")
            
            if not auth:
                logger.debug("No Authorization header found")
                print("No Authorization header found")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required. Please sign in first."
                )

            scheme, credentials = get_authorization_scheme_param(auth)
            logger.debug(f"Auth scheme: {scheme}")
            
            if not scheme or scheme.lower() != "bearer":
                logger.debug(f"Invalid scheme: {scheme}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme. Use Bearer token."
                )

            if not credentials:
                logger.debug("No credentials found")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is missing"
                )

            logger.debug("Returning credentials")
            return credentials

        except HTTPException as e:
            logger.error(f"HTTP Exception: {e.detail}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.detail
            ) 
