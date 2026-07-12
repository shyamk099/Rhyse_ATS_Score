"""Configuration source resolution and immutable settings construction.

Purpose:
    Merge infrastructure sources and construct validated application settings.

TODO:
    Keep source resolution independent from ATS business and Rule Engine content.

Future responsibilities:
    Serve composition wiring with environment-specific infrastructure settings.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Mapping

from pydantic import ValidationError

from ats_engine.infrastructure.configuration.dotenv_loader import DotEnvLoader
from ats_engine.infrastructure.configuration.exceptions import ConfigurationValidationError
from ats_engine.infrastructure.configuration.models import ApplicationSettings, Environment
from ats_engine.infrastructure.configuration.yaml_loader import YamlConfigurationLoader


class ConfigurationResolver:
    """Resolve infrastructure settings from YAML, dotenv, and environment sources."""

    _ENVIRONMENT_KEY = "ATS_ENVIRONMENT"
    _CONFIGURATION_FILE_KEY = "ATS_CONFIGURATION_FILE"
    _ENVIRONMENT_FIELDS = {
        "ATS_APPLICATION_NAME": "application_name",
        "ATS_APPLICATION_VERSION": "application_version",
        "ATS_HOST": "host",
        "ATS_PORT": "port",
        "ATS_API_PREFIX": "api_prefix",
        "ATS_UPLOAD_DIRECTORY": "upload_directory",
        "ATS_TEMPORARY_DIRECTORY": "temporary_directory",
        "ATS_LOG_DIRECTORY": "log_directory",
        "ATS_RULE_DIRECTORY": "rule_directory",
        "ATS_CONFIGURATION_DIRECTORY": "configuration_directory",
        "ATS_ALLOWED_ORIGINS": "allowed_origins",
        "ATS_TIMEZONE": "timezone",
        "ATS_ENCODING": "encoding",
        "ATS_LOGGING_CONFIGURATION_PATH": "logging_configuration_path",
    }

    def __init__(
        self,
        yaml_loader: YamlConfigurationLoader,
        dotenv_loader: DotEnvLoader,
        base_directory: Path | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize resolver dependencies and its path-resolution base directory."""
        self._yaml_loader = yaml_loader
        self._dotenv_loader = dotenv_loader
        self._base_directory = (base_directory or Path.cwd()).resolve()
        self._logger = logger or logging.getLogger(__name__)

    def resolve(
        self,
        environment: Environment | str | None = None,
        *,
        configuration_file: Path | None = None,
        dotenv_file: Path | None = None,
        environment_variables: Mapping[str, str] | None = None,
    ) -> ApplicationSettings:
        """Resolve immutable application settings with deterministic source precedence.

        Source precedence is YAML, dotenv, then supplied process-environment values.

        Args:
            environment: Optional selected environment; otherwise ``ATS_ENVIRONMENT`` is used.
            configuration_file: Optional explicit YAML source path.
            dotenv_file: Optional dotenv source path.
            environment_variables: Optional process-environment mapping for testability.

        Returns:
            Validated immutable infrastructure settings.

        Raises:
            ConfigurationValidationError: If the merged source values are invalid.
        """
        values = dict(environment_variables or os.environ)
        selected_environment = self._resolve_environment(environment, values)
        yaml_path = self._resolve_yaml_path(selected_environment, configuration_file, values)
        dotenv_path = dotenv_file or self._base_directory / ".env"
        self._logger.debug(
            "resolving_configuration",
            extra={"environment": selected_environment.value, "yaml_path": str(yaml_path)},
        )

        yaml_values = self._yaml_loader.load(yaml_path)
        dotenv_values = self._dotenv_loader.load(dotenv_path)
        merged = {**yaml_values, **self._mapped_environment_values(dotenv_values), **self._mapped_environment_values(values)}
        merged["environment"] = selected_environment.value
        normalized = self._normalize_paths(merged)
        try:
            settings = ApplicationSettings.model_validate(normalized)
        except ValidationError as error:
            raise ConfigurationValidationError("invalid infrastructure configuration") from error
        self._logger.debug("configuration_resolved", extra={"environment": settings.environment.value})
        return settings

    def _resolve_environment(self, environment: Environment | str | None, values: Mapping[str, str]) -> Environment:
        candidate = environment or values.get(self._ENVIRONMENT_KEY, Environment.DEVELOPMENT.value)
        try:
            return Environment(candidate)
        except ValueError as error:
            raise ConfigurationValidationError(f"unsupported environment: {candidate}") from error

    def _resolve_yaml_path(
        self,
        environment: Environment,
        configuration_file: Path | None,
        values: Mapping[str, str],
    ) -> Path:
        candidate = configuration_file or values.get(self._CONFIGURATION_FILE_KEY)
        if candidate is not None:
            return self._resolve_path(Path(candidate))
        return self._base_directory / "config" / f"{environment.value}.yaml"

    def _mapped_environment_values(self, values: Mapping[str, str]) -> dict[str, Any]:
        mapped: dict[str, Any] = {}
        for source_key, target_key in self._ENVIRONMENT_FIELDS.items():
            if source_key not in values:
                continue
            value = values[source_key]
            if target_key == "allowed_origins":
                mapped[target_key] = self._parse_allowed_origins(value)
            else:
                mapped[target_key] = value
        return mapped

    def _parse_allowed_origins(self, value: str) -> tuple[str, ...]:
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return tuple(origin.strip() for origin in value.split(",") if origin.strip())
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise ConfigurationValidationError("ATS_ALLOWED_ORIGINS must be a JSON string array or CSV")
        return tuple(parsed)

    def _normalize_paths(self, values: dict[str, Any]) -> dict[str, Any]:
        path_fields = {
            "upload_directory",
            "temporary_directory",
            "log_directory",
            "rule_directory",
            "configuration_directory",
            "logging_configuration_path",
        }
        normalized = dict(values)
        for field_name in path_fields:
            value = normalized.get(field_name)
            if value is not None:
                normalized[field_name] = self._resolve_path(Path(value))
        return normalized

    def _resolve_path(self, path: Path) -> Path:
        return path.resolve() if path.is_absolute() else (self._base_directory / path).resolve()
