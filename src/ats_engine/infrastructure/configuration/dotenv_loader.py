"""Non-mutating .env source loader.

Purpose:
    Read local infrastructure overrides without changing process environment state.

TODO:
    Keep supported syntax intentionally limited and infrastructure-only.

Future responsibilities:
    Provide a source mapping to the configuration resolver.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ats_engine.infrastructure.configuration.exceptions import ConfigurationLoadError


class DotEnvLoader:
    """Load simple KEY=VALUE mappings from an optional dotenv file."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize the loader with an optional structured-logging hook."""
        self._logger = logger or logging.getLogger(__name__)

    def load(self, path: Path) -> dict[str, str]:
        """Load a dotenv file into a mapping without mutating ``os.environ``.

        Args:
            path: Existing dotenv file to parse.

        Returns:
            Parsed environment-variable mapping.

        Raises:
            ConfigurationLoadError: If the file cannot be read or contains invalid syntax.
        """
        self._logger.debug("loading_dotenv_configuration", extra={"path": str(path)})
        if not path.exists():
            return {}
        if not path.is_file():
            raise ConfigurationLoadError(f"dotenv path is not a file: {path}")

        values: dict[str, str] = {}
        try:
            for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigurationLoadError(f"invalid dotenv syntax at line {line_number}")
                key, value = line.split("=", maxsplit=1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if not key:
                    raise ConfigurationLoadError(f"empty dotenv key at line {line_number}")
                values[key] = value
        except OSError as error:
            raise ConfigurationLoadError(f"unable to read dotenv file: {path}") from error

        self._logger.debug("dotenv_configuration_loaded", extra={"path": str(path), "key_count": len(values)})
        return values
