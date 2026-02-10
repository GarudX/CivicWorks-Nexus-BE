import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    ENVIRONMENT: str = "production"
    API_KEY: str = "your-secret-api-key-here"
    MODEL: str = "gpt-4o-mini"
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    MAX_PAGES: int = 30
    DEFAULT_ZOOM: float = 4.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
