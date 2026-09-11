import sys
import logging
from loguru import logger
from app.core.config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    # Remove default loggers
    logging.getLogger().handlers = [InterceptHandler()]
    for log_name in ("uvicorn", "uvicorn.error", "fastapi", "sqlalchemy"):
        mod_logger = logging.getLogger(log_name)
        mod_logger.handlers = [InterceptHandler()]

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": "INFO",
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            },
            {
                "sink": "logs/zombierun.log",
                "rotation": "10 MB",
                "retention": "30 days",
                "level": "DEBUG",
                "compression": "zip",
            }
        ]
    )

__all__ = ["logger", "setup_logging"]
