"""Configuration access service.

Purpose:
    Provide cached, immutable infrastructure settings through an injectable service.

TODO:
    Keep service ownership limited to configuration access and cache coordination.

Future responsibilities:
    Serve future composition and adapter dependencies without exposing source mechanics.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Mapping

from ats_engine.infrastructure.configuration.cache import ConfigurationCache, ConfigurationCacheKey
from ats_engine.infrastructure.configuration.exceptions import ConfigurationValidationError
from ats_engine.infrastructure.configuration.models import ApplicationSettings, Environment
from ats_engine.infrastructure.configuration.resolver import ConfigurationResolver


class ConfigurationService:
    """Access immutable infrastructure settings through an owned cache."""

    def __init__(
        self,
        resolver: ConfigurationResolver,
        cache: ConfigurationCache,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the service with injectable resolver and cache dependencies."""
        self._resolver = resolver
        self._cache = cache
        self._logger = logger or logging.getLogger(__name__)

    def get_settings(
        self,
        environment: Environment | str | None = None,
        *,
        configuration_file: Path | None = None,
        dotenv_file: Path | None = None,
        environment_variables: Mapping[str, str] | None = None,
        refresh: bool = False,
    ) -> ApplicationSettings:
        """Return immutable settings, resolving and caching them when necessary.

        Args:
            environment: Requested environment, or the environment source selection.
            configuration_file: Optional YAML source override.
            dotenv_file: Optional dotenv source override.
            environment_variables: Optional process-environment mapping for testability.
            refresh: Whether to bypass the cached settings value.

        Returns:
            Immutable, validated infrastructure settings.
        """
        values = dict(environment_variables or os.environ)
        selected_environment = self._select_environment(environment, values)
        key = self._cache_key(selected_environment, configuration_file, dotenv_file, values)
        if not refresh:
            cached = self._cache.get(key)
            if cached is not None:
                self._logger.debug("configuration_service_cache_hit", extra={"environment": selected_environment.value})
                return cached
        settings = self._resolver.resolve(
            selected_environment,
            configuration_file=configuration_file,
            dotenv_file=dotenv_file,
            environment_variables=values,
        )
        self._cache.set(key, settings)
        self._logger.debug("configuration_service_resolved", extra={"environment": selected_environment.value})
        return settings

    def clear_cache(self) -> None:
        """Clear configuration cache through the service's explicit public API."""
        self._cache.clear()
        self._logger.debug("configuration_service_cache_cleared")

    def _select_environment(self, environment: Environment | str | None, values: Mapping[str, str]) -> Environment:
        candidate = environment or values.get("ATS_ENVIRONMENT", Environment.DEVELOPMENT.value)
        try:
            return Environment(candidate)
        except ValueError as error:
            raise ConfigurationValidationError(f"unsupported environment: {candidate}") from error

    def _normalized_optional_path(self, path: Path | None) -> Path | None:
        return path.resolve() if path is not None else None

    def _cache_key(
        self,
        environment: Environment,
        configuration_file: Path | None,
        dotenv_file: Path | None,
        values: Mapping[str, str],
    ) -> ConfigurationCacheKey:
        overrides = tuple(sorted((key, value) for key, value in values.items() if key.startswith("ATS_")))
        return (
            environment,
            self._normalized_optional_path(configuration_file),
            self._normalized_optional_path(dotenv_file),
            overrides,
        )
