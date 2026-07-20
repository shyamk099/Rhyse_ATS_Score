"""Unit tests for the ScoringRegistry.

Purpose:
    Verify register, unregister, priority metadata, enabling/disabling, and clear behaviors.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.exceptions import ScorerRegistrationError, UnsupportedScorerError


class DummyScorer(AbstractScorer):
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="DUMMY")
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {}
    def metadata(self) -> dict:
        return {}


class ScoringRegistryTests(unittest.TestCase):
    """Test suite validating ScoringRegistry behaviors."""

    def setUp(self) -> None:
        self.registry = ScoringRegistry()

    def test_register_and_get_scorer(self) -> None:
        self.registry.register("SKILL", DummyScorer, priority=200, enabled=False)
        
        scorer_cls = self.registry.get("SKILL")
        self.assertEqual(DummyScorer, scorer_cls)

        meta = self.registry.get_metadata("SKILL")
        self.assertEqual(200, meta["priority"])
        self.assertFalse(meta["enabled"])

    def test_register_raises_on_invalid_scorer_class(self) -> None:
        class NotAScorer:
            pass

        with self.assertRaises(ScorerRegistrationError):
            self.registry.register("INVALID", NotAScorer)  # type: ignore

    def test_unregister_removes_scorer(self) -> None:
        self.registry.register("SKILL", DummyScorer)
        self.assertIn("SKILL", self.registry.list())

        self.registry.unregister("SKILL")
        self.assertNotIn("SKILL", self.registry.list())

        with self.assertRaises(UnsupportedScorerError):
            self.registry.get("SKILL")

    def test_unregister_raises_on_missing(self) -> None:
        with self.assertRaises(UnsupportedScorerError):
            self.registry.unregister("MISSING")

    def test_clear_removes_all_scorers(self) -> None:
        self.registry.register("SKILL", DummyScorer)
        self.registry.register("EXPERIENCE", DummyScorer)
        self.assertEqual(2, len(self.registry.list()))

        self.registry.clear()
        self.assertEqual(0, len(self.registry.list()))
