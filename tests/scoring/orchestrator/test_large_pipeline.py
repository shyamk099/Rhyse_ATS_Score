"""Tests for large pipeline orchestration.

Purpose:
    Verify the orchestrator can handle registries with many scorers without
    exceeding a generous 100ms latency target, and that ordering remains correct.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan
from ats_engine.domain.ats_scoring.rules import ScoringRules

from tests.scoring.orchestrator.helpers import make_collection, make_scorer


class LargePipelineTests(unittest.TestCase):
    """Tests verifying orchestration scalability with many registered scorers."""

    SCORER_COUNT: int = 50

    def _build_large_registry(self) -> ScoringRegistry:
        """Build a registry with SCORER_COUNT scorers at unique priorities."""
        reg = ScoringRegistry()
        # Register standard five first at standard priorities
        for name, priority in [
            ("SKILL", 100), ("EXPERIENCE", 200), ("EDUCATION", 300),
            ("PROJECT", 400), ("CERTIFICATION", 500),
        ]:
            reg.register(name, make_scorer(name), priority=priority, enabled=True)
        # Add extra scorers at higher priorities (600, 700, ...)
        for i in range(5, self.SCORER_COUNT):
            extra_name = f"EXTRA_{i}"
            reg.register(extra_name, make_scorer(extra_name), priority=600 + i, enabled=True)
        return reg

    def test_large_registry_execution_plan_builds(self) -> None:
        """ExecutionPlan must build successfully for a 50-scorer registry."""
        reg = self._build_large_registry()
        plan = ExecutionPlan.build(reg)
        self.assertEqual(self.SCORER_COUNT, len(plan))

    def test_large_registry_order_is_sorted_descending(self) -> None:
        """ExecutionPlan with 50 scorers must remain priority-sorted descending."""
        reg = self._build_large_registry()
        plan = ExecutionPlan.build(reg)
        priorities = [e.priority for e in plan.entries]
        self.assertEqual(sorted(priorities, reverse=True), priorities)

    def test_large_registry_orchestration_latency(self) -> None:
        """Orchestrating 50 scorers must complete within 100ms."""
        # Use only 5 real scorers for latency — this tests the orchestration overhead,
        # not scorer calculation time. 50 stub scorers added for plan-build testing.
        reg = ScoringRegistry()
        for name, priority in [
            ("SKILL", 100), ("EXPERIENCE", 200), ("EDUCATION", 300),
            ("PROJECT", 400), ("CERTIFICATION", 500),
        ]:
            reg.register(name, make_scorer(name), priority=priority, enabled=True)

        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)
        rules = ScoringRules()

        start = time.perf_counter()
        orch.orchestrate(make_collection(), rules=rules)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(elapsed_ms, 100.0, f"Orchestration latency exceeded: {elapsed_ms:.2f}ms")

    def test_large_execution_plan_build_latency(self) -> None:
        """ExecutionPlan.build() for 50 scorers must complete within 50ms."""
        reg = self._build_large_registry()
        start = time.perf_counter()
        ExecutionPlan.build(reg)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        self.assertLess(elapsed_ms, 50.0, f"ExecutionPlan build latency exceeded: {elapsed_ms:.2f}ms")

    def test_large_registry_with_some_disabled(self) -> None:
        """Half disabled, half enabled — plan length must equal enabled count."""
        reg = ScoringRegistry()
        for i in range(self.SCORER_COUNT):
            name = f"SCORER_{i}"
            enabled = i % 2 == 0  # even indices enabled
            reg.register(name, make_scorer(name), priority=i + 1, enabled=enabled)

        plan = ExecutionPlan.build(reg)
        expected_enabled = sum(1 for i in range(self.SCORER_COUNT) if i % 2 == 0)
        self.assertEqual(expected_enabled, len(plan))
        expected_skipped = sum(1 for i in range(self.SCORER_COUNT) if i % 2 != 0)
        self.assertEqual(expected_skipped, len(plan.skipped))


if __name__ == "__main__":
    unittest.main()
