from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from middleware import APIKeyMiddleware, LoggingMiddleware
from routes import location_router, health_router
from config.settings import get_settings
from utils.logger import logger

settings = get_settings()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(
    title="Map Rendering API",
    description="""
    FastAPI service for extracting location information from PDF maps using OpenAI Vision.
    
    ## Features
    - Extract location names and linear feet measurements from map PDFs
    - Match locations with addresses from routing PDFs
    - Generate Google Maps links for each location
    - Development mode with hardcoded data to save API costs
    
    ## Authentication
    All endpoints (except /health, /docs, /redoc) require an `X-API-Key` header.
    Click the **Authorize** button and enter your API key.
    
    ## Environment Modes
    - **development**: Uses hardcoded data, no OpenAI API calls
    - **production**: Processes PDFs using OpenAI Vision API
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(APIKeyMiddleware)

app.include_router(health_router)
app.include_router(location_router)

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Map Rendering API Starting...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Model: {settings.MODEL}")
    logger.info(f"OpenAI API Key configured: {bool(settings.OPENAI_API_KEY)}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Map Rendering API Shutting Down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
