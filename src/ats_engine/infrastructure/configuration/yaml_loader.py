"""YAML source loader for infrastructure configuration.

Purpose:
    Load environment-specific infrastructure settings from YAML documents.

TODO:
    Do not add ATS rule loading to this module.

Future responsibilities:
    Supply validated source mappings to the configuration resolver.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from ats_engine.infrastructure.configuration.exceptions import (
    ConfigurationFileNotFoundError,
    ConfigurationLoadError,
)


class YamlConfigurationLoader:
    """Load one YAML mapping for infrastructure configuration."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize the loader with an optional structured-logging hook."""
        self._logger = logger or logging.getLogger(__name__)

    def load(self, path: Path) -> dict[str, Any]:
        """Load and validate one YAML mapping.

        Args:
            path: Required YAML file containing a top-level mapping.

        Returns:
            Parsed YAML mapping.

        Raises:
            ConfigurationFileNotFoundError: If the YAML file does not exist.
            ConfigurationLoadError: If YAML is malformed or not a mapping.
        """
        self._logger.debug("loading_yaml_configuration", extra={"path": str(path)})
        if not path.exists():
            raise ConfigurationFileNotFoundError(f"configuration file does not exist: {path}")
        if not path.is_file():
            raise ConfigurationLoadError(f"configuration path is not a file: {path}")
        try:
            parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            raise ConfigurationLoadError(f"unable to load YAML configuration: {path}") from error
        if not isinstance(parsed, dict):
            raise ConfigurationLoadError("YAML configuration must contain a top-level mapping")
        self._logger.debug("yaml_configuration_loaded", extra={"path": str(path), "key_count": len(parsed)})
        return parsed
