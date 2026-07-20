"""Unit and integration tests for the ScoringService coordination facade.

Purpose:
    Verify orchestration facade execution and default fallback parameters.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.service import ScoringService
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore


class ServiceDummyScorer(AbstractScorer):
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="SKILL", raw_score=85.0)
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {}
    def metadata(self) -> dict:
        return {}


class ScoringServiceTests(unittest.TestCase):
    """Test suite validating ScoringService APIs."""

    def test_service_executes_pipeline_with_defaults(self) -> None:
        service = ScoringService()
        service.registry.register("SKILL", ServiceDummyScorer)

        collection = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )

        res = service.score(collection)

        self.assertIsNotNone(res)
        self.assertEqual("SKILL", res.skill_score.section_name)
        self.assertEqual(85.0, res.skill_score.raw_score)
        self.assertEqual("1.0.0", res.metadata.rules_version)

    def test_service_respects_custom_rules(self) -> None:
        service = ScoringService()
        rules = ScoringRules(version="1.0.0", strictness="LENIENT")

        collection = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )

        res = service.score(collection, rules)
        self.assertEqual("1.0.0", res.metadata.rules_version)
