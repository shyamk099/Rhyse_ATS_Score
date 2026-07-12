"""Typed exceptions for infrastructure configuration.

Purpose:
    Distinguish configuration source, load, and validation failures.

TODO:
    Keep exceptions free from ATS business semantics.

Future responsibilities:
    Support presentation-layer error translation through approved adapters.

Handbook reference:
    Book 01 - System Architecture.
"""


class ConfigurationError(Exception):
    """Base exception for configuration infrastructure failures."""


class ConfigurationFileNotFoundError(ConfigurationError):
    """Raised when a required infrastructure configuration file is absent."""


class ConfigurationLoadError(ConfigurationError):
    """Raised when a configuration source cannot be parsed safely."""


class ConfigurationValidationError(ConfigurationError):
    """Raised when assembled infrastructure configuration is invalid."""
