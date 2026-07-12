"""Custom logging infrastructure exception classes.

Purpose:
    Define logging-specific errors without referencing ATS domain logic.
"""

class LoggingError(Exception):
    """Base exception for all logging infrastructure errors."""


class LoggingConfigurationError(LoggingError):
    """Raised when the logging system configuration fails or is invalid."""
