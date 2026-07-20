"""Tests for PrioritizationEngine thread safety.

Purpose:
    Verify concurrent prioritization engine process execution does not cause race conditions.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine


class PrioritizationThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety of PrioritizationEngine."""

    THREAD_COUNT: int = 20

    def setUp(self) -> None:
        self.engine = PrioritizationEngine()
        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
            ),
        ]
        self.raw_result = RecommendationResult(
            context=RecommendationContext(),
            recommendations=tuple(recs),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )

    def test_concurrent_processing_is_isolated(self) -> None:
        """All threads executing process() concurrently must succeed with independent DTO lists."""
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = self.engine.process(self.raw_result)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for r in results:
            self.assertEqual(2, r.total_recommendations)

        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))


if __name__ == "__main__":
    unittest.main()
