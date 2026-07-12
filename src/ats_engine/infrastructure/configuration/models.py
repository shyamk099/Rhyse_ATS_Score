"""Immutable Pydantic models for infrastructure configuration.

Purpose:
    Validate application runtime settings without representing ATS business rules.

TODO:
    Add fields only when an approved infrastructure milestone requires them.

Future responsibilities:
    Provide typed settings to outer-layer adapters and composition wiring.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Environment(str, Enum):
    """Supported infrastructure deployment environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class ApplicationSettings(BaseModel):
    """Validated, immutable infrastructure settings for one runtime environment."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    application_name: str = Field(min_length=1)
    application_version: str = Field(min_length=1)
    environment: Environment
    host: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)
    api_prefix: str = Field(min_length=1)
    upload_directory: Path
    temporary_directory: Path
    log_directory: Path
    rule_directory: Path
    configuration_directory: Path
    allowed_origins: tuple[str, ...] = ()
    timezone: str = Field(min_length=1)
    encoding: str = Field(min_length=1)
    logging_configuration_path: Path

    @field_validator(
        "upload_directory",
        "temporary_directory",
        "log_directory",
        "rule_directory",
        "configuration_directory",
        "logging_configuration_path",
        mode="before",
    )
    @classmethod
    def validate_absolute_path(cls, value: str | Path) -> Path:
        """Validate that resolved infrastructure paths are absolute."""
        path = Path(value)
        if not path.is_absolute():
            raise ValueError("infrastructure paths must be absolute")
        return path

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def validate_allowed_origins(cls, value: object) -> tuple[str, ...]:
        """Normalize allowed origins to an immutable tuple."""
        if value is None:
            return ()
        if isinstance(value, str):
            return tuple(origin.strip() for origin in value.split(",") if origin.strip())
        if isinstance(value, (list, tuple)) and all(isinstance(origin, str) for origin in value):
            return tuple(origin.strip() for origin in value if origin.strip())
        raise ValueError("allowed_origins must be a string list or comma-separated string")

    @model_validator(mode="after")
    def validate_api_prefix(self) -> ApplicationSettings:
        """Validate the API transport prefix is a normalized absolute path."""
        if not self.api_prefix.startswith("/"):
            raise ValueError("api_prefix must start with '/'")
        if self.api_prefix != "/" and self.api_prefix.endswith("/"):
            raise ValueError("api_prefix must not end with '/' unless it is root")
        return self
