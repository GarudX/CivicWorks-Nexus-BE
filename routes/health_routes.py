from fastapi import APIRouter
from models.schemas import HealthResponse
from config.settings import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Check if the API is running and get environment information"
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version="1.0.0"
    )
