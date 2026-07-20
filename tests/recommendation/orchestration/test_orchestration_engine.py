"""Tests for RecommendationOrchestrationEngine.

Purpose:
    Verify orchestration post-processor executing builder, validator, and stats.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult, PrioritizationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine
from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult


class OrchestrationEngineTests(unittest.TestCase):
    """Test suite validating RecommendationOrchestrationEngine execution."""

    def setUp(self) -> None:
        self.engine = RecommendationOrchestrationEngine()

    def test_process_empty_prioritized_result(self) -> None:
        """Processing an empty prioritized result must succeed with 0 recommendations."""
        prioritized = PrioritizedRecommendationResult(
            recommendations=(),
            statistics=PrioritizationStatistics(
                execution_time_ms=0.1,
                recommendations_processed=0,
                high_priority=0,
                medium_priority=0,
                low_priority=0,
                average_priority=0.0,
                average_impact=0.0,
                average_confidence=0.0,
                success=True,
            ),
            total_recommendations=0,
            high_priority=0,
            medium_priority=0,
            low_priority=0,
        )
        res = self.engine.process(prioritized)

        self.assertIsInstance(res, OrchestratedRecommendationResult)
        self.assertEqual(0, res.total_recommendations)
        self.assertEqual(0, len(res.recommendations))
        self.assertEqual(0, len(res.grouped_recommendations))
        self.assertEqual(0, len(res.recommendations_by_section))
        self.assertTrue(res.statistics.success)

    def test_process_single_prioritized_recommendation(self) -> None:
        """Processing a single recommendation DTO must group and index correctly."""
        rec = Recommendation(
            recommendation_id="SKILL_MISSING_PYTHON",
            section="skill",
            category="SKILL_MISSING",
            title="Python is missing",
            description="Python missing.",
            priority=100,
            impact=1.0,
            confidence=1.0,
        )
        prioritized = PrioritizedRecommendationResult(
            recommendations=(rec,),
            statistics=PrioritizationStatistics(
                execution_time_ms=0.1,
                recommendations_processed=1,
                high_priority=1,
                medium_priority=0,
                low_priority=0,
                average_priority=100.0,
                average_impact=1.0,
                average_confidence=1.0,
                success=True,
            ),
            total_recommendations=1,
            high_priority=1,
            medium_priority=0,
            low_priority=0,
        )
        res = self.engine.process(prioritized)

        self.assertEqual(1, res.total_recommendations)
        self.assertEqual(1, len(res.recommendations_by_section["skill"]))
        self.assertEqual("SKILL_MISSING_PYTHON", res.recommendations_by_section["skill"][0].recommendation_id)
        self.assertEqual(1, len(res.recommendations_by_priority["High"]))
        self.assertEqual(0, len(res.recommendations_by_priority["Medium"]))
        self.assertEqual(0, len(res.recommendations_by_priority["Low"]))


if __name__ == "__main__":
    unittest.main()
