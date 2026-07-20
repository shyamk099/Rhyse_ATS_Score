"""Tests for RecommendationOrchestrationEngine performance latency.

Purpose:
    Verify that processing recommendations for 1000 contexts sequentially
    completes within 100ms.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult, PrioritizationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine


class OrchestrationLargeDatasetTests(unittest.TestCase):
    """Latency performance tests validating orchestration execution budget."""

    ITERATIONS: int = 1000

    def test_large_dataset_orchestration_latency(self) -> None:
        """1000 sequential process() calls must execute within a 100ms budget."""
        engine = RecommendationOrchestrationEngine()

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
        prioritized = PrioritizedRecommendationResult(
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

        start = time.perf_counter()
        for _ in range(self.ITERATIONS):
            engine.process(prioritized)
        duration_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(
            duration_ms,
            100.0,
            f"Orchestration engine scale latency target exceeded: 1000 runs took {duration_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
