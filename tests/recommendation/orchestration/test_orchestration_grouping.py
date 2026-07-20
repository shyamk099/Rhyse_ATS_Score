"""Tests for RecommendationOrchestrationEngine grouping logic.

Purpose:
    Verify that orchestration groups by section, category, and priority correctly.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult, PrioritizationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine


class OrchestrationGroupingTests(unittest.TestCase):
    """Test suite validating grouping details."""

    def test_grouping_categories_sections_and_priorities(self) -> None:
        """Engine must construct clean mappings grouped by category, section, and priority tier."""
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
        engine = RecommendationOrchestrationEngine()
        res = engine.process(prioritized)

        # Mappings checks
        self.assertEqual(tuple(res.recommendations_by_section.keys()), ("skill", "project"))
        self.assertEqual(res.recommendations_by_section["skill"][0].recommendation_id, "SKILL_MISSING_PYTHON")

        self.assertEqual(tuple(res.grouped_recommendations.keys()), ("SKILL_MISSING", "PROJECT_MISSING"))
        self.assertEqual(res.grouped_recommendations["SKILL_MISSING"][0].recommendation_id, "SKILL_MISSING_PYTHON")

        self.assertEqual(len(res.recommendations_by_priority["High"]), 1)
        self.assertEqual(res.recommendations_by_priority["High"][0].recommendation_id, "SKILL_MISSING_PYTHON")
        self.assertEqual(len(res.recommendations_by_priority["Medium"]), 1)
        self.assertEqual(res.recommendations_by_priority["Medium"][0].recommendation_id, "PROJ_MISSING_KAFKA")


if __name__ == "__main__":
    unittest.main()
