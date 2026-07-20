"""Tests for factory integration with ResumeIntelligenceSummaryEngine.

Purpose:
    Verify the default factory registers the summary engine in the pipeline.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine


class SummaryFactoryTests(unittest.TestCase):
    """Test suite validating factory registration of summary engine."""

    def test_default_engine_has_summary_post_processor(self) -> None:
        """Default engine must include ResumeIntelligenceSummaryEngine post-processor."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        post_processor_types = [type(p) for p in engine.post_processors]
        self.assertIn(ResumeIntelligenceSummaryEngine, post_processor_types)

    def test_summary_engine_is_last_post_processor(self) -> None:
        """ResumeIntelligenceSummaryEngine must be the last post-processor in the pipeline."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertIsInstance(engine.post_processors[-1], ResumeIntelligenceSummaryEngine)

    def test_pipeline_has_three_post_processors(self) -> None:
        """Pipeline must have exactly 3 post-processors: Prioritization, Orchestration, Summary."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(3, len(engine.post_processors))

    def test_pipeline_order(self) -> None:
        """Post-processors must be in order: Prioritization, Orchestration, Summary."""
        from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine
        from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine

        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertIsInstance(engine.post_processors[0], PrioritizationEngine)
        self.assertIsInstance(engine.post_processors[1], RecommendationOrchestrationEngine)
        self.assertIsInstance(engine.post_processors[2], ResumeIntelligenceSummaryEngine)


if __name__ == "__main__":
    unittest.main()
