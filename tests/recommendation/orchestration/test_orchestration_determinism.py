"""Tests for RecommendationOrchestrationEngine determinism.

Purpose:
    Verify repeated orchestration process runs yield identical output.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult, PrioritizationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine


class OrchestrationDeterminismTests(unittest.TestCase):
    """Test suite validating orchestration output determinism."""

    REPETITIONS: int = 25

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

    def test_processing_is_fully_deterministic(self) -> None:
        """Repeated engine.process() calls must yield identical orchestrated lists and groupings."""
        first = self.engine.process(self.prioritized)
        first_ids = [r.recommendation_id for r in first.recommendations]

        for _ in range(self.REPETITIONS - 1):
            res = self.engine.process(self.prioritized)
            res_ids = [r.recommendation_id for r in res.recommendations]
            self.assertEqual(first_ids, res_ids)
            self.assertEqual(len(first.grouped_recommendations), len(res.grouped_recommendations))


if __name__ == "__main__":
    unittest.main()
