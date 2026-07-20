"""Tests for ScoreOrchestrator core orchestration behaviour.

Purpose:
    Verify that ScoreOrchestrator correctly delegates to the pipeline,
    returns an immutable ScoreResult, and does not mutate the result.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.exceptions import OrchestrationError

from tests.scoring.orchestrator.helpers import make_collection, make_scorer


class OrchestratorCoreTests(unittest.TestCase):
    """Test suite for ScoreOrchestrator core delegation and result integrity."""

    def _make_orchestrator(self, registry: ScoringRegistry) -> ScoreOrchestrator:
        pipeline = ScoringPipeline(registry=registry)
        return ScoreOrchestrator(pipeline=pipeline, registry=registry)

    def _make_registry(self) -> ScoringRegistry:
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL", 30.0), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE", 20.0), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION", 15.0), priority=300, enabled=True)
        reg.register("PROJECT", make_scorer("PROJECT", 10.0), priority=400, enabled=True)
        reg.register("CERTIFICATION", make_scorer("CERTIFICATION", 8.0), priority=500, enabled=True)
        return reg

    def test_orchestrate_returns_score_result(self) -> None:
        """orchestrate() must return a ScoreResult instance."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        self.assertIsInstance(result, ScoreResult)

    def test_orchestrate_returns_immutable_result(self) -> None:
        """ScoreResult returned by orchestrate() must be frozen (pydantic)."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        with self.assertRaises(Exception):
            # pydantic frozen model raises on attribute assignment
            result.overall_score = 99.0  # type: ignore[misc]

    def test_orchestrate_delegates_to_pipeline(self) -> None:
        """Section scores should match what the registered scorers produce."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        self.assertIsNotNone(result.skill_score)
        self.assertEqual(30.0, result.skill_score.raw_score)
        self.assertIsNotNone(result.experience_score)
        self.assertEqual(20.0, result.experience_score.raw_score)

    def test_orchestrate_does_not_compute_overall_score(self) -> None:
        """overall_score must remain None — orchestrator must not aggregate."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        self.assertIsNone(result.overall_score)

    def test_orchestrate_populates_statistics(self) -> None:
        """Statistics block must be populated after orchestrate()."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        self.assertIsNotNone(result.statistics)
        self.assertGreater(result.statistics.total_sections, 0)

    def test_orchestrate_populates_metadata(self) -> None:
        """Metadata block must be populated with pipeline_version and generated_at."""
        orch = self._make_orchestrator(self._make_registry())
        result = orch.orchestrate(make_collection())
        self.assertIsNotNone(result.metadata)
        self.assertTrue(result.metadata.pipeline_version)
        self.assertTrue(result.metadata.generated_at)

    def test_orchestrate_exposes_last_orchestration_stats(self) -> None:
        """last_orchestration_stats must be populated after orchestrate()."""
        orch = self._make_orchestrator(self._make_registry())
        orch.orchestrate(make_collection())
        stats = orch.last_orchestration_stats
        self.assertIn("execution_time_ms", stats)
        self.assertIn("success", stats)
        self.assertTrue(stats["success"])

    def test_orchestrate_with_explicit_rules(self) -> None:
        """orchestrate() must accept explicit ScoringRules and pass them through."""
        orch = self._make_orchestrator(self._make_registry())
        rules = ScoringRules(version="1.0.0", strictness="LENIENT")
        result = orch.orchestrate(make_collection(), rules=rules)
        self.assertIsInstance(result, ScoreResult)

    def test_orchestrate_pipeline_failure_raises_orchestration_error(self) -> None:
        """A fatal pipeline failure must be wrapped in OrchestrationError."""
        from tests.scoring.orchestrator.helpers import make_failing_scorer
        reg = ScoringRegistry()
        reg.register("SKILL", make_failing_scorer("SKILL"), priority=100, enabled=True)
        orch = self._make_orchestrator(reg)
        rules = ScoringRules(strictness="STRICT")
        with self.assertRaises(OrchestrationError):
            orch.orchestrate(make_collection(), rules=rules)

    def test_orchestrator_pipeline_property(self) -> None:
        """pipeline property must return the injected ScoringPipeline."""
        reg = self._make_registry()
        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)
        self.assertIs(pipeline, orch.pipeline)

    def test_orchestrator_registry_property(self) -> None:
        """registry property must return the injected ScoringRegistry."""
        reg = self._make_registry()
        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)
        self.assertIs(reg, orch.registry)


if __name__ == "__main__":
    unittest.main()
