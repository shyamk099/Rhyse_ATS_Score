"""Infrastructure logging public API.

Purpose:
    Expose structured, context-aware logging utilities for the entire application.
"""

from ats_engine.infrastructure.logging.adapter import LoggingContextAdapter
from ats_engine.infrastructure.logging.context import LoggingContext
from ats_engine.infrastructure.logging.exceptions import (
    LoggingConfigurationError,
    LoggingError,
)
from ats_engine.infrastructure.logging.factory import LoggerFactory
from ats_engine.infrastructure.logging.formatter import StructuredFormatter
from ats_engine.infrastructure.logging.performance import log_execution_time
from ats_engine.infrastructure.logging.service import LoggingService

__all__ = [
    "LoggerFactory",
    "LoggingContext",
    "LoggingContextAdapter",
    "LoggingConfigurationError",
    "LoggingError",
    "LoggingService",
    "StructuredFormatter",
    "log_execution_time",
]
