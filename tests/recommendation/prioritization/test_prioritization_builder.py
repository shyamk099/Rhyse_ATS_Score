"""Tests for PrioritizationBuilder.

Purpose:
    Verify builder copies and updates priority DTO fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.prioritization_builder import PrioritizationBuilder
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class PrioritizationBuilderTests(unittest.TestCase):
    """Test suite validating builder functionality."""

    def setUp(self) -> None:
        self.rules = PrioritizationRules()

    def test_prioritize_and_sort_applies_profiles(self) -> None:
        """Builder must correctly copy recommendations and fill them with rules profiles."""
        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
            ),
        ]
        res = PrioritizationBuilder.prioritize_and_sort(recs, self.rules)

        self.assertEqual(2, len(res))
        # Sorted: Python (priority 100) first, Kafka (priority 80) second
        self.assertEqual("SKILL_MISSING_PYTHON", res[0].recommendation_id)
        self.assertEqual(100, res[0].priority)
        self.assertEqual(1.0, res[0].impact)

        self.assertEqual("PROJ_MISSING_KAFKA", res[1].recommendation_id)
        self.assertEqual(80, res[1].priority)
        self.assertEqual(0.75, res[1].impact)


if __name__ == "__main__":
    unittest.main()
