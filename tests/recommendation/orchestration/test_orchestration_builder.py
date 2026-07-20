"""Tests for RecommendationOrchestrationBuilder.

Purpose:
    Verify grouping outputs of builder preserve priority sorting sequence.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.orchestration_builder import RecommendationOrchestrationBuilder
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class OrchestrationBuilderTests(unittest.TestCase):
    """Test suite validating builder functionality."""

    def test_grouping_and_ordering(self) -> None:
        """Builder must group recommendations and preserve the list order inside groups."""
        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=100,
                impact=1.0,
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
                priority=80,
                impact=0.75,
            ),
        ]
        by_sec = RecommendationOrchestrationBuilder.build_section_groups(recs)
        self.assertEqual(2, len(by_sec))
        self.assertEqual("SKILL_MISSING_PYTHON", by_sec["skill"][0].recommendation_id)
        self.assertEqual("PROJ_MISSING_KAFKA", by_sec["project"][0].recommendation_id)

        rules = PrioritizationRules()
        by_pri = RecommendationOrchestrationBuilder.build_priority_groups(recs, rules)
        self.assertEqual(1, len(by_pri["High"]))
        self.assertEqual(1, len(by_pri["Medium"]))
        self.assertEqual(0, len(by_pri["Low"]))


if __name__ == "__main__":
    unittest.main()
