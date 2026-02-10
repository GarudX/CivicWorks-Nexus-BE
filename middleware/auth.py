from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from config.settings import get_settings
from utils.logger import logger

settings = get_settings()


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
            return await call_next(request)
        
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            logger.warning(f"Missing API key for request to {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-API-Key header"
            )
        
        if api_key != settings.API_KEY:
            logger.warning(f"Invalid API key attempt for request to {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key"
            )
        
        logger.info(f"Authenticated request to {request.url.path}")
        response = await call_next(request)
        return response
