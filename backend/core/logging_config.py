"""
Nova AI — Structured Logging Configuration
Uses Loguru for rich, structured logging with file rotation.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from backend.core.config import settings


def setup_logging() -> None:
    """Configure Loguru logger for Nova AI."""

    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # ── Console handler (rich colored output) ────────────────────────────────
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,
        diagnose=settings.DEBUG,
    )

    # ── File handler (rotating JSON logs) ────────────────────────────────────
    logger.add(
        settings.LOG_FILE,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        rotation=settings.LOG_ROTATION,
        retention="30 days",
        compression="zip",
        serialize=False,
        enqueue=True,  # Thread-safe async logging
    )

    logger.info(
        "Nova AI logging initialized",
        env=settings.APP_ENV,
        version=settings.APP_VERSION,
        level=settings.LOG_LEVEL,
    )


class NovaLogger:
    """Named logger factory for module-level logging."""

    def __init__(self, name: str) -> None:
        self._logger = logger.bind(module=name)

    def info(self, msg: str, **kwargs: object) -> None:
        self._logger.info(msg, **kwargs)

    def debug(self, msg: str, **kwargs: object) -> None:
        self._logger.debug(msg, **kwargs)

    def warning(self, msg: str, **kwargs: object) -> None:
        self._logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs: object) -> None:
        self._logger.error(msg, **kwargs)

    def critical(self, msg: str, **kwargs: object) -> None:
        self._logger.critical(msg, **kwargs)

    def exception(self, msg: str, **kwargs: object) -> None:
        self._logger.exception(msg, **kwargs)
