"""Tests for RecommendationOrchestrationEngine Factory integration.

Purpose:
    Verify factory configures the default engine with RecommendationOrchestrationEngine.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine


class OrchestrationFactoryTests(unittest.TestCase):
    """Test suite validating factory integration with Orchestration Engine."""

    def test_factory_includes_orchestration_engine(self) -> None:
        """create_default_recommendation_engine() must include RecommendationOrchestrationEngine after PrioritizationEngine."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(3, len(engine.post_processors))
        self.assertIsInstance(engine.post_processors[1], RecommendationOrchestrationEngine)


if __name__ == "__main__":
    unittest.main()
