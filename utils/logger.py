import logging
import os
from logging.handlers import RotatingFileHandler
from config.settings import get_settings

settings = get_settings()


def is_serverless() -> bool:
    """Check if running in a serverless environment (Vercel, AWS Lambda, etc.)"""
    return bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))


def setup_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if not is_serverless():
        try:
            os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
            file_handler = RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=10485760,
                backupCount=5
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, PermissionError):
            pass
    
    return logger


logger = setup_logger("map_rendering_api")
