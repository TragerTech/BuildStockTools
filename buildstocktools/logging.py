"""Logging configuration for BuildStockTools."""
from __future__ import annotations

from loguru import logger

_DEFAULT_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"


def configure_logging(level: str = "INFO") -> None:
    """Configure loguru's global logger with the given level."""
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=level.upper(), format=_DEFAULT_FORMAT)


__all__ = ["configure_logging", "logger"]

