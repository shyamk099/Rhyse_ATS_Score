"""Integration and pipeline tests for the ScoringPipeline.

Purpose:
    Verify validator integration, sequential priorities execution, disabled skipping,
    exception handling under STRICT rules, and result DTO construction.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.exceptions import ScoringPipelineError


class DummySkillScorer(AbstractScorer):
    """Mock Skill Scorer."""
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="SKILL", raw_score=95.0, maximum_score=100.0)
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {"processed": 1}
    def metadata(self) -> dict:
        return {"version": "1.0.0"}


class DummyExperienceScorer(AbstractScorer):
    """Mock Experience Scorer."""
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="EXPERIENCE", raw_score=80.0, maximum_score=100.0)
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {"processed": 1}
    def metadata(self) -> dict:
        return {"version": "1.0.0"}


class FailingScorer(AbstractScorer):
    """Scorer that fails validation or execution."""
    def validate(self, context: ScoringContext) -> None:
        raise ValueError("Intentional validation fail")
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="EDUCATION")
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {}
    def metadata(self) -> dict:
        return {}


class ScoringPipelineTests(unittest.TestCase):
    """Test suite validating ScoringPipeline execution logic."""

    def setUp(self) -> None:
        self.registry = ScoringRegistry()
        self.pipeline = ScoringPipeline(registry=self.registry)
        self.collection = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )

    def test_pipeline_executes_registered_scorers(self) -> None:
        self.registry.register("SKILL", DummySkillScorer, priority=100)
        self.registry.register("EXPERIENCE", DummyExperienceScorer, priority=200)

        rules = ScoringRules()
        res = self.pipeline.execute(self.collection, rules)

        self.assertIsNotNone(res)
        self.assertEqual("SKILL", res.skill_score.section_name)
        self.assertEqual(95.0, res.skill_score.raw_score)

        self.assertEqual("EXPERIENCE", res.experience_score.section_name)
        self.assertEqual(80.0, res.experience_score.raw_score)

        # verify statistics
        self.assertEqual(5, res.statistics.total_sections)
        self.assertIn("SKILL", res.statistics.executed_scorers)
        self.assertIn("EXPERIENCE", res.statistics.executed_scorers)
        self.assertEqual(0, len(res.statistics.failed_scorers))

    def test_pipeline_skips_disabled_scorers(self) -> None:
        self.registry.register("SKILL", DummySkillScorer, enabled=False)
        self.registry.register("EXPERIENCE", DummyExperienceScorer, enabled=True)

        rules = ScoringRules()
        res = self.pipeline.execute(self.collection, rules)

        self.assertIn("SKILL", res.statistics.skipped_scorers)
        self.assertIn("EXPERIENCE", res.statistics.executed_scorers)

    def test_pipeline_strict_mode_raises_on_scorer_failure(self) -> None:
        self.registry.register("EDUCATION", FailingScorer)
        rules = ScoringRules(strictness="STRICT")

        with self.assertRaises(ScoringPipelineError):
            self.pipeline.execute(self.collection, rules)

    def test_pipeline_lenient_mode_records_warning_on_scorer_failure(self) -> None:
        self.registry.register("EDUCATION", FailingScorer)
        rules = ScoringRules(strictness="LENIENT")

        res = self.pipeline.execute(self.collection, rules)
        self.assertIn("EDUCATION", res.statistics.failed_scorers)
        self.assertEqual(1, len(res.statistics.failed_scorers))
        self.assertEqual(1, len(res.warnings))
        self.assertEqual("INVALID", res.validation_summary["status"])
