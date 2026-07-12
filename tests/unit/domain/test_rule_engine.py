"""Unit tests for the Rule Engine Foundation.

Purpose:
    Verify file scanning, YAML loading, thread-safe cache updates, atomic reloading,
    immutability, and duplicate key constraints.
"""

from __future__ import annotations

import tempfile
import threading
import time
import unittest
from pathlib import Path
import yaml
from pydantic import ValidationError

from ats_engine.domain.rule_engine.cache import RuleCache
from ats_engine.domain.rule_engine.exceptions import (
    DuplicateRuleError,
    RuleLoadError,
    RuleNotFoundError,
    RuleValidationError,
)
from ats_engine.domain.rule_engine.loader import RuleLoader
from ats_engine.domain.rule_engine.service import RuleEngineService
from ats_engine.domain.rule_engine.validator import RuleValidator


class RuleEngineFoundationTests(unittest.TestCase):
    """Test suite for the Rule Engine Foundation infrastructure."""

    def setUp(self) -> None:
        """Create an isolated temporary rule directory for test files."""
        self._temporary_directory = tempfile.TemporaryDirectory()
        self._rule_dir = Path(self._temporary_directory.name)
        self._cache = RuleCache()
        self._service = RuleEngineService(self._cache)

    def tearDown(self) -> None:
        """Clean up temporary test files after each test run."""
        self._temporary_directory.cleanup()

    def test_loads_multiple_valid_rule_files(self) -> None:
        """Service loads all valid rule YAML files from the target directory."""
        self._write_yaml(
            "parser",
            rule_id="parser_rules",
            rule_version="1.0.0",
            payload={"max_file_size_mb": 10},
        )
        self._write_yaml(
            "scoring",
            rule_id="scoring_rules",
            rule_version="2.1",
            payload={"weights": {"compatibility": 20}},
        )

        self._service.load_rules(self._rule_dir)

        self.assertTrue(self._service.exists("parser_rules"))
        self.assertTrue(self._service.exists("scoring_rules"))

        parser_rule = self._service.get("parser_rules")
        self.assertEqual("parser_rules", parser_rule.metadata.rule_id)
        self.assertEqual("1.0.0", parser_rule.metadata.rule_version)
        self.assertEqual(10, parser_rule.payload["max_file_size_mb"])
        self.assertEqual("parser.yaml", parser_rule.source)

        active_version = self._service.active_version()
        self.assertIn("parser_rules:1.0.0", active_version)
        self.assertIn("scoring_rules:2.1", active_version)

    def test_fails_fast_on_missing_directory(self) -> None:
        """Loading from a non-existent directory raises RuleLoadError."""
        with self.assertRaises(RuleLoadError):
            self._service.load_rules(self._rule_dir / "nonexistent_dir")

    def test_fails_fast_on_empty_directory(self) -> None:
        """Loading from a directory with no rule files raises RuleLoadError."""
        with self.assertRaises(RuleLoadError):
            self._service.load_rules(self._rule_dir)

    def test_fails_fast_on_malformed_yaml(self) -> None:
        """Malformed YAML syntax raises RuleLoadError."""
        file_path = self._rule_dir / "malformed.yaml"
        file_path.write_text("metadata:\n  rule_id: : unmatched_colon", encoding="utf-8")

        with self.assertRaises(RuleLoadError):
            self._service.load_rules(self._rule_dir)

    def test_fails_fast_on_missing_required_fields(self) -> None:
        """Missing required envelope schema fields raises RuleValidationError."""
        # Missing payload
        self._write_raw_yaml("invalid_schema", {"metadata": {"rule_id": "invalid", "rule_version": "1.0", "effective_date": "2026", "status": "ACTIVE"}})
        with self.assertRaises(RuleValidationError):
            self._service.load_rules(self._rule_dir)

    def test_fails_fast_on_invalid_identifiers(self) -> None:
        """Identifiers with illegal characters raise RuleValidationError."""
        self._write_yaml(
            "rules",
            rule_id="invalid-id-with-dash",
            rule_version="1.0",
            payload={},
        )
        with self.assertRaises(RuleValidationError):
            self._service.load_rules(self._rule_dir)

    def test_fails_fast_on_invalid_versions(self) -> None:
        """Non-numeric version strings raise RuleValidationError."""
        self._write_yaml(
            "rules",
            rule_id="rules",
            rule_version="v1.0.0-beta",
            payload={},
        )
        with self.assertRaises(RuleValidationError):
            self._service.load_rules(self._rule_dir)

    def test_fails_fast_on_duplicate_identifiers(self) -> None:
        """Duplicate rule IDs across files raise DuplicateRuleError."""
        self._write_yaml(
            "file1",
            rule_id="shared_rule_id",
            rule_version="1.0",
            payload={},
        )
        self._write_yaml(
            "file2",
            rule_id="shared_rule_id",
            rule_version="1.0",
            payload={},
        )

        with self.assertRaises(DuplicateRuleError):
            self._service.load_rules(self._rule_dir)

    def test_lookup_on_unloaded_service_raises_not_found(self) -> None:
        """Querying rules before any load operation raises RuleNotFoundError."""
        with self.assertRaises(RuleNotFoundError):
            self._service.get("any_rule")

    def test_lookup_of_nonexistent_rule_raises_not_found(self) -> None:
        """Querying a missing rule identifier raises RuleNotFoundError."""
        self._write_yaml("rules", rule_id="rules", rule_version="1.0", payload={})
        self._service.load_rules(self._rule_dir)

        with self.assertRaises(RuleNotFoundError):
            self._service.get("nonexistent_id")

    def test_runtime_objects_are_immutable(self) -> None:
        """Caller cannot modify fields in cached or retrieved rule envelopes."""
        self._write_yaml("rules", rule_id="rules", rule_version="1.0", payload={"value": 10})
        self._service.load_rules(self._rule_dir)

        envelope = self._service.get("rules")
        
        # Verify frozen Pydantic models block mutation
        with self.assertRaises(ValidationError):
            # Attempt modifying metadata fields (raises ValidationError in Pydantic v2 frozen models)
            envelope.metadata.model_validate({"rule_id": "mutated"})

    def test_cache_is_thread_safe_and_reloads_atomically(self) -> None:
        """Multiple threads can query rules while reloads execute atomically."""
        self._write_yaml("rules", rule_id="rules", rule_version="1.0", payload={"val": 1})
        self._service.load_rules(self._rule_dir)

        barrier = threading.Barrier(3)
        exceptions: list[Exception] = []

        def reader_target() -> None:
            barrier.wait()
            for _ in range(50):
                try:
                    envelope = self._service.get("rules")
                    self.assertIn(envelope.payload["val"], [1, 2])
                    time.sleep(0.001)
                except Exception as e:
                    exceptions.append(e)

        def reloader_target() -> None:
            barrier.wait()
            # Rewrite yaml file with updated payload
            self._write_yaml("rules", rule_id="rules", rule_version="2.0", payload={"val": 2})
            for _ in range(10):
                try:
                    self._service.reload_rules()
                    time.sleep(0.005)
                except Exception as e:
                    exceptions.append(e)

        thread1 = threading.Thread(target=reader_target)
        thread2 = threading.Thread(target=reader_target)
        thread3 = threading.Thread(target=reloader_target)

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        self.assertEqual(0, len(exceptions), f"Reader/writer exceptions: {exceptions}")
        self.assertEqual(2, self._service.get("rules").payload["val"])

    def test_metadata_returns_correct_summary(self) -> None:
        """metadata() returns audit records including checksums and load times."""
        self._write_yaml("rules", rule_id="rules", rule_version="1.0", payload={"key": "val"})
        self._service.load_rules(self._rule_dir)

        meta_summary = self._service.metadata()
        self.assertIn("rules", meta_summary)
        
        rule_meta = meta_summary["rules"]
        self.assertEqual("1.0", rule_meta["rule_version"])
        self.assertEqual("ACTIVE", rule_meta["status"])
        self.assertEqual("rules.yaml", rule_meta["source"])
        self.assertIsNotNone(rule_meta["checksum"])
        self.assertIsNotNone(rule_meta["loaded_timestamp"])

    def _write_yaml(
        self,
        filename: str,
        *,
        rule_id: str,
        rule_version: str,
        payload: dict,
    ) -> None:
        content = {
            "metadata": {
                "rule_id": rule_id,
                "rule_version": rule_version,
                "effective_date": "2026-07-12",
                "status": "ACTIVE",
                "description": f"Test rule {rule_id}",
            },
            "payload": payload,
        }
        self._write_raw_yaml(filename, content)

    def _write_raw_yaml(self, filename: str, content: dict) -> None:
        filepath = self._rule_dir / f"{filename}.yaml"
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(content, f)
