"""Infrastructure configuration public API.

Purpose:
    Expose immutable infrastructure settings and their access service.

TODO:
    Keep this package independent from ATS business and Rule Engine behavior.

Future responsibilities:
    Support approved infrastructure adapters through validated runtime settings.

Handbook reference:
    Book 01 - System Architecture.
"""

from ats_engine.infrastructure.configuration.exceptions import (
    ConfigurationError,
    ConfigurationFileNotFoundError,
    ConfigurationLoadError,
    ConfigurationValidationError,
)
from ats_engine.infrastructure.configuration.models import ApplicationSettings, Environment
from ats_engine.infrastructure.configuration.service import ConfigurationService

__all__ = [
    "ApplicationSettings",
    "ConfigurationError",
    "ConfigurationFileNotFoundError",
    "ConfigurationLoadError",
    "ConfigurationService",
    "ConfigurationValidationError",
    "Environment",
]
