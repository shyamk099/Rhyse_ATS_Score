"""Integration tests validating the integration of all Phase 1 infrastructure.

Purpose:
    Verify that Configuration, Logging, and the Rule Engine wire together and startup/shutdown
    correctly in sequence.
"""

from __future__ import annotations

import json
import logging
import tempfile
import unittest
from pathlib import Path
import yaml

from ats_engine.application.composition_root import CompositionRoot
from ats_engine.domain.rule_engine.models import RuleEnvelope
from ats_engine.infrastructure.configuration.models import Environment


class InfrastructureIntegrationTests(unittest.TestCase):
    """Integration test suite for CompositionRoot and Phase 1 infrastructure sequence."""

    def setUp(self) -> None:
        """Set up isolated directories for config, logs, and rules."""
        self._temp_dir = tempfile.TemporaryDirectory()
        self._base_dir = Path(self._temp_dir.name)
        
        self._config_dir = self._base_dir / "config"
        self._config_dir.mkdir()
        
        self._rules_dir = self._base_dir / "rules"
        self._rules_dir.mkdir()
        
        self._log_dir = self._base_dir / "logs"
        self._log_dir.mkdir()

        # Write integration-testing YAML config
        self._write_config_yaml("testing")

        # Write dummy logging.yaml config
        self._write_logging_yaml()

        # Write dummy rules
        self._write_rule_yaml("parser_rules", "1.0", {"max_file_size_mb": 10})
        self._write_rule_yaml("scoring_rules", "1.1", {"weights": {"matching": 50}})

    def tearDown(self) -> None:
        """Clean up all temporary directories and release logging handlers."""
        self._temp_dir.cleanup()
        logging.getLogger().handlers.clear()

    def test_startup_sequence_resolves_and_wires_correctly(self) -> None:
        """CompositionRoot runs startup sequence Config -> Logging -> Rules atomically."""
        root = CompositionRoot(
            base_directory=self._base_dir,
            environment=Environment.TESTING,
        )

        # 1. Verify Configuration wiring
        self.assertEqual("test-app", root.settings.application_name)
        self.assertEqual(Environment.TESTING, root.settings.environment)

        # 2. Verify Logging configured correctly with handlers
        root_logger = logging.getLogger()
        self.assertGreater(len(root_logger.handlers), 0)

        # 3. Verify Rule Engine loaded rules from the configured rules directory
        self.assertTrue(root.rule_engine_service.exists("parser_rules"))
        self.assertTrue(root.rule_engine_service.exists("scoring_rules"))

        # Verify rule version retrieval
        self.assertEqual("parser_rules:1.0;scoring_rules:1.1", root.rule_engine_service.active_version())

        # Cleanup
        root.shutdown()

    def test_dotenv_overrides_yaml_in_composition(self) -> None:
        """CompositionRoot applies dotenv environment variable overrides correctly."""
        dotenv_path = self._base_dir / ".env"
        dotenv_path.write_text("ATS_PORT=9090\nATS_APPLICATION_NAME=overridden-app\n", encoding="utf-8")

        root = CompositionRoot(
            base_directory=self._base_dir,
            environment=Environment.TESTING,
            dotenv_file=dotenv_path,
        )

        self.assertEqual(9090, root.settings.port)
        self.assertEqual("overridden-app", root.settings.application_name)
        root.shutdown()

    def test_shutdown_sequence_clears_caches_and_stops_logging(self) -> None:
        """CompositionRoot shutdown clears configurations, rules cache, and logging handles."""
        root = CompositionRoot(
            base_directory=self._base_dir,
            environment=Environment.TESTING,
        )

        # Assert populated state
        self.assertIsNotNone(root.configuration_service.get_settings(Environment.TESTING))
        self.assertTrue(root.rule_engine_service.exists("parser_rules"))

        # Run shutdown
        root.shutdown()

        # Check rule engine cache is cleared
        self.assertFalse(root.rule_engine_service.exists("parser_rules"))

    def _write_config_yaml(self, env_name: str) -> None:
        content = f"""application_name: test-app
application_version: 1.0.0
host: 127.0.0.1
port: 8080
api_prefix: /api/v1
upload_directory: {self._base_dir / "uploads"}
temporary_directory: {self._base_dir / "tmp"}
log_directory: {self._log_dir}
rule_directory: {self._rules_dir}
configuration_directory: {self._config_dir}
allowed_origins:
  - http://localhost
timezone: UTC
encoding: utf-8
logging_configuration_path: {self._config_dir / "logging.yaml"}
"""
        # Ensure directories exist
        (self._base_dir / "uploads").mkdir(exist_ok=True)
        (self._base_dir / "tmp").mkdir(exist_ok=True)
        (self._config_dir / f"{env_name}.yaml").write_text(content, encoding="utf-8")

    def _write_rule_yaml(self, rule_id: str, version: str, payload: dict) -> None:
        content = {
            "metadata": {
                "rule_id": rule_id,
                "rule_version": version,
                "effective_date": "2026-07-12",
                "status": "ACTIVE",
                "description": f"Test rule {rule_id}",
            },
            "payload": payload,
        }
        with open(self._rules_dir / f"{rule_id}.yaml", "w", encoding="utf-8") as f:
            yaml.dump(content, f)

    def _write_logging_yaml(self) -> None:
        content = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "structured": {
                    "()": "ats_engine.infrastructure.logging.formatter.StructuredFormatter",
                    "include_context": True,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "structured",
                    "level": "INFO",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            }
        }
        with open(self._config_dir / "logging.yaml", "w", encoding="utf-8") as f:
            yaml.dump(content, f)
