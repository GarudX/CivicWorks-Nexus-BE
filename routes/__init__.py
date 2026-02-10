from .location_routes import router as location_router
from .health_routes import router as health_router

__all__ = ["location_router", "health_router"]
