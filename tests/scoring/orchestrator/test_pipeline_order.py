"""Tests for scorer execution pipeline ordering.

Purpose:
    Verify that the orchestrator executes scorers in priority-descending order
    and that ExecutionPlan reflects this exact order for the five standard sections.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan

from tests.scoring.orchestrator.helpers import make_collection, make_scorer


class PipelineOrderTests(unittest.TestCase):
    """Tests verifying deterministic execution ordering through ExecutionPlan."""

    def _make_full_registry(self) -> ScoringRegistry:
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION"), priority=300, enabled=True)
        reg.register("PROJECT", make_scorer("PROJECT"), priority=400, enabled=True)
        reg.register("CERTIFICATION", make_scorer("CERTIFICATION"), priority=500, enabled=True)
        return reg

    def test_execution_plan_order_is_descending_by_priority(self) -> None:
        """ExecutionPlan entries must be sorted priority-descending."""
        plan = ExecutionPlan.build(self._make_full_registry())
        priorities = [e.priority for e in plan.entries]
        self.assertEqual(sorted(priorities, reverse=True), priorities)

    def test_execution_plan_order_is_certification_first_skill_last(self) -> None:
        """Default registry: CERTIFICATION(500) executes first, SKILL(100) last."""
        plan = ExecutionPlan.build(self._make_full_registry())
        order = plan.execution_order
        self.assertEqual("CERTIFICATION", order[0])
        self.assertEqual("SKILL", order[-1])

    def test_standard_five_section_execution_order(self) -> None:
        """The five standard sections must execute in exact priority-descending order."""
        plan = ExecutionPlan.build(self._make_full_registry())
        expected = ("CERTIFICATION", "PROJECT", "EDUCATION", "EXPERIENCE", "SKILL")
        self.assertEqual(expected, plan.execution_order)

    def test_single_scorer_order_trivially_correct(self) -> None:
        """A single scorer produces a plan with that scorer alone."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        plan = ExecutionPlan.build(reg)
        self.assertEqual(("SKILL",), plan.execution_order)

    def test_two_scorers_higher_priority_first(self) -> None:
        """Among two scorers, the one with higher priority appears first."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=999, enabled=True)
        plan = ExecutionPlan.build(reg)
        self.assertEqual("EXPERIENCE", plan.entries[0].name)
        self.assertEqual("SKILL", plan.entries[1].name)

    def test_orchestrator_produces_section_scores_for_all_five(self) -> None:
        """After orchestration, all five section scores must be non-None."""
        reg = self._make_full_registry()
        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)
        result = orch.orchestrate(make_collection())
        self.assertIsNotNone(result.skill_score)
        self.assertIsNotNone(result.experience_score)
        self.assertIsNotNone(result.education_score)
        self.assertIsNotNone(result.project_score)
        self.assertIsNotNone(result.certification_score)

    def test_execution_plan_order_stable_across_multiple_builds(self) -> None:
        """Building ExecutionPlan multiple times from the same registry yields same order."""
        reg = self._make_full_registry()
        plan1 = ExecutionPlan.build(reg)
        plan2 = ExecutionPlan.build(reg)
        self.assertEqual(plan1.execution_order, plan2.execution_order)


if __name__ == "__main__":
    unittest.main()
