"""Tests for RecommendationOrchestrationEngine thread safety.

Purpose:
    Verify concurrent orchestration engine process execution does not cause race conditions.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult, PrioritizationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine


class OrchestrationThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety of RecommendationOrchestrationEngine."""

    THREAD_COUNT: int = 20

    def setUp(self) -> None:
        self.engine = RecommendationOrchestrationEngine()
        rec1 = Recommendation(
            recommendation_id="SKILL_MISSING_PYTHON",
            section="skill",
            category="SKILL_MISSING",
            title="Python missing",
            description="Python missing.",
            priority=100,
            impact=1.0,
            confidence=1.0,
        )
        rec2 = Recommendation(
            recommendation_id="PROJ_MISSING_KAFKA",
            section="project",
            category="PROJECT_MISSING",
            title="Kafka project missing",
            description="Kafka project missing.",
            priority=80,
            impact=0.75,
            confidence=1.0,
        )
        self.prioritized = PrioritizedRecommendationResult(
            recommendations=(rec1, rec2),
            statistics=PrioritizationStatistics(
                execution_time_ms=0.1,
                recommendations_processed=2,
                high_priority=1,
                medium_priority=1,
                low_priority=0,
                average_priority=90.0,
                average_impact=0.875,
                average_confidence=1.0,
                success=True,
            ),
            total_recommendations=2,
            high_priority=1,
            medium_priority=1,
            low_priority=0,
        )

    def test_concurrent_processing_is_isolated(self) -> None:
        """All threads executing process() concurrently must succeed with independent OrchestratedRecommendationResult DTO lists."""
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = self.engine.process(self.prioritized)
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
