"""Tests for PrioritizationEngine.

Purpose:
    Verify prioritization flow coordinating rules, builder, validator, and stats.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult


class PrioritizationEngineTests(unittest.TestCase):
    """Test suite validating PrioritizationEngine execution."""

    def setUp(self) -> None:
        self.engine = PrioritizationEngine()

    def test_process_empty_recommendations(self) -> None:
        """Processing an empty RecommendationResult must succeed with 0 prioritized DTOs."""
        raw_res = RecommendationResult(
            context=RecommendationContext(),
            recommendations=(),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )
        res = self.engine.process(raw_res)

        self.assertIsInstance(res, PrioritizedRecommendationResult)
        self.assertEqual(0, res.total_recommendations)
        self.assertEqual(0, len(res.recommendations))
        self.assertEqual(0, res.high_priority)
        self.assertEqual(0, res.medium_priority)
        self.assertEqual(0, res.low_priority)
        self.assertTrue(res.statistics.success)

    def test_process_single_recommendation(self) -> None:
        """Processing a single recommendation DTO must apply profiles and return correctly."""
        rec = Recommendation(
            recommendation_id="SKILL_MISSING_PYTHON",
            section="skill",
            category="SKILL_MISSING",
            title="Python is missing",
            description="Python missing.",
        )
        raw_res = RecommendationResult(
            context=RecommendationContext(),
            recommendations=(rec,),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )
        res = self.engine.process(raw_res)

        self.assertEqual(1, res.total_recommendations)
        self.assertEqual(100, res.recommendations[0].priority)
        self.assertEqual(1.0, res.recommendations[0].impact)
        self.assertEqual(1.0, res.recommendations[0].confidence)
        self.assertEqual(1, res.high_priority)
        self.assertEqual(0, res.medium_priority)
        self.assertEqual(0, res.low_priority)


if __name__ == "__main__":
    unittest.main()
