"""Tests for PrioritizationStatisticsBuilder.

Purpose:
    Verify statistics builder fields and calculation correctness.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.prioritization_statistics_builder import PrioritizationStatisticsBuilder
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class PrioritizationStatisticsTests(unittest.TestCase):
    """Test suite validating statistics compilation."""

    def test_statistics_calculations(self) -> None:
        """Verify built stats DTO fields and averages are calculated correctly."""
        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=100,
                impact=1.0,
                confidence=1.0,
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
                priority=80,
                impact=0.75,
                confidence=0.90,
            ),
        ]
        rules = PrioritizationRules()
        stats = PrioritizationStatisticsBuilder.build(recs, rules, execution_time_ms=12.34)

        self.assertEqual(12.34, stats.execution_time_ms)
        self.assertEqual(2, stats.recommendations_processed)
        self.assertEqual(1, stats.high_priority)  # Python (100)
        self.assertEqual(1, stats.medium_priority)  # Kafka (80)
        self.assertEqual(0, stats.low_priority)
        self.assertEqual(90.0, stats.average_priority)
        self.assertEqual(0.875, stats.average_impact)
        self.assertEqual(0.95, stats.average_confidence)
        self.assertTrue(stats.success)


if __name__ == "__main__":
    unittest.main()
