"""Tests for orchestration determinism.

Purpose:
    Verify that repeated calls to orchestrate() and ExecutionPlan.build()
    produce identical, consistent results regardless of call count.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline

from tests.scoring.orchestrator.helpers import make_collection, make_scorer


class OrchestratorDeterminismTests(unittest.TestCase):
    """Tests verifying deterministic ordering and result stability."""

    REPETITIONS: int = 25

    def _make_full_registry(self) -> ScoringRegistry:
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL", 30.0), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE", 20.0), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION", 15.0), priority=300, enabled=True)
        reg.register("PROJECT", make_scorer("PROJECT", 10.0), priority=400, enabled=True)
        reg.register("CERTIFICATION", make_scorer("CERTIFICATION", 8.0), priority=500, enabled=True)
        return reg

    def test_execution_plan_order_is_identical_across_builds(self) -> None:
        """ExecutionPlan built 25 times must always yield the same execution_order."""
        reg = self._make_full_registry()
        first_order = ExecutionPlan.build(reg).execution_order
        for _ in range(self.REPETITIONS - 1):
            order = ExecutionPlan.build(reg).execution_order
            self.assertEqual(first_order, order)

    def test_orchestrate_section_scores_are_identical(self) -> None:
        """Repeated orchestrate() calls must produce identical section raw scores."""
        reg = self._make_full_registry()
        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)

        first = orch.orchestrate(make_collection())
        for _ in range(self.REPETITIONS - 1):
            result = orch.orchestrate(make_collection())
            self.assertEqual(first.skill_score.raw_score, result.skill_score.raw_score)
            self.assertEqual(first.experience_score.raw_score, result.experience_score.raw_score)
            self.assertEqual(first.education_score.raw_score, result.education_score.raw_score)
            self.assertEqual(first.project_score.raw_score, result.project_score.raw_score)
            self.assertEqual(first.certification_score.raw_score, result.certification_score.raw_score)

    def test_orchestrate_overall_score_always_none(self) -> None:
        """overall_score must be None on every call — never computed by accident."""
        orch = ScoringFactory.create_default_orchestrator()
        for _ in range(self.REPETITIONS):
            result = orch.orchestrate(make_collection())
            self.assertIsNone(result.overall_score)

    def test_execution_plan_skipped_is_stable(self) -> None:
        """Skipped scorer list must be identical across all builds."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        first_skipped = ExecutionPlan.build(reg).skipped
        for _ in range(self.REPETITIONS - 1):
            skipped = ExecutionPlan.build(reg).skipped
            self.assertEqual(first_skipped, skipped)

    def test_validator_produces_consistent_outcome_across_calls(self) -> None:
        """ScoreOrchestratorValidator must pass or fail consistently for the same registry."""
        from ats_engine.domain.ats_scoring.orchestrator.validator import ScoreOrchestratorValidator
        reg = self._make_full_registry()
        # All calls should pass without exception
        for _ in range(self.REPETITIONS):
            ScoreOrchestratorValidator.validate(reg)

    def test_statistics_keys_are_stable_across_calls(self) -> None:
        """Orchestration statistics must have identical keys on every call."""
        orch = ScoringFactory.create_default_orchestrator()
        orch.orchestrate(make_collection())
        first_keys = set(orch.last_orchestration_stats.keys())
        for _ in range(self.REPETITIONS - 1):
            orch.orchestrate(make_collection())
            keys = set(orch.last_orchestration_stats.keys())
            self.assertEqual(first_keys, keys)


if __name__ == "__main__":
    unittest.main()
