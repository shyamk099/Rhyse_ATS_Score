"""Unit tests for infrastructure configuration.

Purpose:
    Verify source loading, validation, overrides, and caching without ATS behavior.

TODO:
    Extend only with approved configuration requirements.

Future responsibilities:
    Guard the configuration boundary against infrastructure regressions.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ats_engine.infrastructure.configuration.cache import ConfigurationCache
from ats_engine.infrastructure.configuration.exceptions import (
    ConfigurationFileNotFoundError,
    ConfigurationValidationError,
)
from ats_engine.infrastructure.configuration.models import Environment
from ats_engine.infrastructure.configuration.resolver import ConfigurationResolver
from ats_engine.infrastructure.configuration.service import ConfigurationService
from ats_engine.infrastructure.configuration.dotenv_loader import DotEnvLoader
from ats_engine.infrastructure.configuration.yaml_loader import YamlConfigurationLoader


class ConfigurationServiceTests(unittest.TestCase):
    """Verify the configuration service without external dependencies."""

    def setUp(self) -> None:
        """Create isolated configuration sources and service dependencies."""
        self._temporary_directory = tempfile.TemporaryDirectory()
        self._base_directory = Path(self._temporary_directory.name)
        self._config_directory = self._base_directory / "config"
        self._config_directory.mkdir()
        self._write_yaml("development", port=8000)
        self._write_yaml("testing", port=8001)
        resolver = ConfigurationResolver(
            YamlConfigurationLoader(),
            DotEnvLoader(),
            base_directory=self._base_directory,
        )
        self._service = ConfigurationService(resolver, ConfigurationCache())

    def tearDown(self) -> None:
        """Release temporary source files after each isolated test."""
        self._temporary_directory.cleanup()

    def test_loads_selected_environment_yaml(self) -> None:
        """Selected environment loads its YAML infrastructure values."""
        settings = self._service.get_settings(Environment.TESTING)

        self.assertEqual(Environment.TESTING, settings.environment)
        self.assertEqual(8001, settings.port)
        self.assertEqual((self._base_directory / "uploads").resolve(), settings.upload_directory)

    def test_loads_dotenv_overrides(self) -> None:
        """Dotenv values override YAML without mutating process environment."""
        dotenv_path = self._base_directory / ".env"
        dotenv_path.write_text("ATS_HOST=localhost\nATS_PORT=9000\n", encoding="utf-8")

        settings = self._service.get_settings(Environment.DEVELOPMENT, dotenv_file=dotenv_path)

        self.assertEqual("localhost", settings.host)
        self.assertEqual(9000, settings.port)

    def test_process_environment_overrides_dotenv_and_yaml(self) -> None:
        """Supplied environment mapping has the highest infrastructure precedence."""
        dotenv_path = self._base_directory / ".env"
        dotenv_path.write_text("ATS_PORT=9000\n", encoding="utf-8")

        settings = self._service.get_settings(
            Environment.DEVELOPMENT,
            dotenv_file=dotenv_path,
            environment_variables={"ATS_PORT": "9100"},
        )

        self.assertEqual(9100, settings.port)

    def test_cache_does_not_share_injected_environment_overrides(self) -> None:
        """Cache keys keep caller-provided infrastructure overrides isolated."""
        overridden = self._service.get_settings(
            Environment.DEVELOPMENT,
            environment_variables={"ATS_PORT": "9100"},
        )
        default = self._service.get_settings(Environment.DEVELOPMENT)

        self.assertEqual(9100, overridden.port)
        self.assertEqual(8000, default.port)

    def test_rejects_invalid_configuration(self) -> None:
        """Invalid infrastructure fields raise a typed validation exception."""
        self._write_yaml("production", port=0)

        with self.assertRaises(ConfigurationValidationError):
            self._service.get_settings(Environment.PRODUCTION)

    def test_rejects_missing_required_configuration(self) -> None:
        """Absent YAML source raises a typed file-not-found exception."""
        with self.assertRaises(ConfigurationFileNotFoundError):
            self._service.get_settings(Environment.PRODUCTION)

    def test_caches_immutable_settings_until_refresh(self) -> None:
        """Repeated lookups return cached settings until explicit refresh."""
        initial = self._service.get_settings(Environment.DEVELOPMENT)
        self._write_yaml("development", port=8123)

        cached = self._service.get_settings(Environment.DEVELOPMENT)
        refreshed = self._service.get_settings(Environment.DEVELOPMENT, refresh=True)

        self.assertIs(initial, cached)
        self.assertEqual(8000, cached.port)
        self.assertEqual(8123, refreshed.port)

    def _write_yaml(self, environment: str, *, port: int) -> None:
        content = f"""application_name: test-application
application_version: 1.0.0
host: 127.0.0.1
port: {port}
api_prefix: /api/v1
upload_directory: uploads
temporary_directory: tmp
log_directory: logs
rule_directory: rules
configuration_directory: config
allowed_origins:
  - http://testserver
timezone: UTC
encoding: utf-8
logging_configuration_path: config/logging.yaml
"""
        (self._config_directory / f"{environment}.yaml").write_text(content, encoding="utf-8")
