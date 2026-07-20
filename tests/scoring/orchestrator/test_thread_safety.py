"""Tests for thread-safe concurrent orchestration.

Purpose:
    Verify that multiple threads can invoke ScoreOrchestrator.orchestrate()
    concurrently and each receives an independent, correct ScoreResult.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult

from tests.scoring.orchestrator.helpers import make_collection


class OrchestratorThreadSafetyTests(unittest.TestCase):
    """Tests verifying ScoreOrchestrator is safe for concurrent use."""

    THREAD_COUNT: int = 20

    def test_concurrent_orchestrations_produce_valid_results(self) -> None:
        """All threads must receive a valid ScoreResult with no exceptions."""
        orch = ScoringFactory.create_default_orchestrator()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = orch.orchestrate(make_collection())
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for result in results:
            self.assertIsInstance(result, ScoreResult)

    def test_concurrent_results_are_independent(self) -> None:
        """Results from concurrent threads must not share mutable state."""
        orch = ScoringFactory.create_default_orchestrator()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = orch.orchestrate(make_collection())
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors))
        # Each result is a distinct pydantic frozen object
        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))

    def test_concurrent_overall_score_always_none(self) -> None:
        """Concurrent orchestrations must never compute an overall_score."""
        orch = ScoringFactory.create_default_orchestrator()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = orch.orchestrate(make_collection())
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors))
        for result in results:
            if result is not None:
                self.assertIsNone(result.overall_score)

    def test_concurrent_execution_plan_builds_are_consistent(self) -> None:
        """Concurrent ExecutionPlan.build() calls must produce identical orders."""
        from ats_engine.domain.ats_scoring.registry import ScoringRegistry
        from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan
        from tests.scoring.orchestrator.helpers import make_scorer

        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION"), priority=300, enabled=True)

        plans: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def build_plan(index: int) -> None:
            try:
                plans[index] = ExecutionPlan.build(reg)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=build_plan, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors))
        expected_order = plans[0].execution_order
        for plan in plans:
            self.assertEqual(expected_order, plan.execution_order)


if __name__ == "__main__":
    unittest.main()
