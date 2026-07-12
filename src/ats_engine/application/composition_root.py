"""Composition Root for infrastructure wiring.

Purpose:
    Provide the centralized composition and initialization sequence for all Phase 1 infrastructure.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Mapping, Optional

from ats_engine.domain.rule_engine.cache import RuleCache
from ats_engine.domain.rule_engine.service import RuleEngineService
from ats_engine.infrastructure.configuration.cache import ConfigurationCache
from ats_engine.infrastructure.configuration.models import ApplicationSettings, Environment
from ats_engine.infrastructure.configuration.resolver import ConfigurationResolver
from ats_engine.infrastructure.configuration.service import ConfigurationService
from ats_engine.infrastructure.configuration.dotenv_loader import DotEnvLoader
from ats_engine.infrastructure.configuration.yaml_loader import YamlConfigurationLoader
from ats_engine.infrastructure.logging.service import LoggingService


class CompositionRoot:
    """Composition Root responsible for wiring and initializing infrastructure components."""

    def __init__(
        self,
        *,
        base_directory: Optional[Path] = None,
        environment: Optional[Environment] = None,
        dotenv_file: Optional[Path] = None,
        environment_variables: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Initialize and wire the core system configuration, logging, and rules.

        Args:
            base_directory: Root project directory for path resolution.
            environment: Current deployment environment.
            dotenv_file: Custom override dotenv path.
            environment_variables: Dictionary of env variables for overrides.
        """
        # 1. Initialize Configuration Service
        resolver = ConfigurationResolver(
            YamlConfigurationLoader(),
            DotEnvLoader(),
            base_directory=base_directory,
        )
        self._configuration_service = ConfigurationService(resolver, ConfigurationCache())
        
        # Load settings
        self._settings = self._configuration_service.get_settings(
            environment=environment,
            dotenv_file=dotenv_file,
            environment_variables=environment_variables,
        )

        # 2. Configure Logging using loaded settings
        LoggingService.configure(
            log_directory=self._settings.log_directory,
            logging_configuration_path=self._settings.logging_configuration_path,
        )

        # 3. Create Rule Engine Service & load rules from the configured directory
        self._rule_cache = RuleCache()
        self._rule_engine_service = RuleEngineService(self._rule_cache)
        
        # Load rules atomically (only if the directory exists and contains rules)
        if self._settings.rule_directory.is_dir():
            try:
                self._rule_engine_service.load_rules(self._settings.rule_directory)
            except Exception as error:
                # Log load failure but preserve class composition state for verification
                logging.getLogger(__name__).warning(
                    f"rule_engine_startup_load_skipped: {error}"
                )

    @property
    def settings(self) -> ApplicationSettings:
        """Return the active ApplicationSettings."""
        return self._settings

    @property
    def configuration_service(self) -> ConfigurationService:
        """Return the wired ConfigurationService."""
        return self._configuration_service

    @property
    def rule_engine_service(self) -> RuleEngineService:
        """Return the wired RuleEngineService."""
        return self._rule_engine_service

    def shutdown(self) -> None:
        """Perform system shutdown in correct sequence."""
        # 1. Clear caches
        self._configuration_service.clear_cache()
        self._rule_cache.clear()
        
        # 2. Shutdown Logging
        LoggingService.shutdown()
