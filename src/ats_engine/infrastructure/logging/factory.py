"""Thread-safe factory for creating and managing logger instances.

Purpose:
    Provide centralized access to configured, context-aware loggers.
"""

from __future__ import annotations

import logging
import threading
from typing import ClassVar

from ats_engine.infrastructure.logging.adapter import LoggingContextAdapter


class LoggerFactory:
    """Thread-safe factory to retrieve and cache LoggingContextAdapter instances."""

    _lock: ClassVar[threading.Lock] = threading.Lock()
    _loggers: ClassVar[dict[str, LoggingContextAdapter]] = {}

    @classmethod
    def get_logger(cls, name: str) -> LoggingContextAdapter:
        """Get or create a cached, context-aware adapted logger.

        Args:
            name: The logger name (typically __name__).
        """
        with cls._lock:
            if name not in cls._loggers:
                base_logger = logging.getLogger(name)
                cls._loggers[name] = LoggingContextAdapter(base_logger)
            return cls._loggers[name]

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the factory cache. Useful for testing."""
        with cls._lock:
            cls._loggers.clear()
