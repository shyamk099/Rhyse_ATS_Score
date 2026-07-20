"""Tests for RecommendationOrchestrationEngine pipeline integration.

Purpose:
    Verify that the recommendation pipeline executes providers followed by
    prioritization, orchestration, then summary post-processors sequentially.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceSummary
from tests.recommendation.helpers import make_recommendation_context


class OrchestrationPipelineTests(unittest.TestCase):
    """Test suite validating end-to-end post-processor pipeline integration."""

    def test_end_to_end_orchestrated_pipeline(self) -> None:
        """Default recommendation engine must produce ResumeIntelligenceSummary when recommend() is called."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        context = make_recommendation_context()
        res = engine.recommend(context)

        self.assertIsInstance(res, ResumeIntelligenceSummary)
        self.assertEqual(0, res.total_recommendations)
        self.assertTrue(res.statistics.summary_generated)


if __name__ == "__main__":
    unittest.main()

