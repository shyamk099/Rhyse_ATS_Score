"""Unit tests for the ScoringFactory.

Purpose:
    Verify registry, rules, and pipeline default instantiations.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.rules import ScoringRules


class ScoringFactoryTests(unittest.TestCase):
    """Test suite validating ScoringFactory dependency-injection creation logic."""

    def test_create_default_registry(self) -> None:
        registry = ScoringFactory.create_default_registry()
        self.assertIsInstance(registry, ScoringRegistry)

    def test_create_default_rules(self) -> None:
        rules = ScoringFactory.create_default_rules()
        self.assertIsInstance(rules, ScoringRules)
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)

    def test_create_default_pipeline(self) -> None:
        registry = ScoringFactory.create_default_registry()
        pipeline = ScoringFactory.create_default_pipeline(registry)
        self.assertIsInstance(pipeline, ScoringPipeline)
        self.assertEqual(registry, pipeline._registry)
