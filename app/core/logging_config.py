"""Logging configuration"""
import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging() -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger("helpvia")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)
    file_handler = logging.FileHandler(log_dir / "helpvia_api.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
