"""Tests for OrchestrationStatisticsBuilder.

Purpose:
    Verify statistics builder compiles workload, category metrics, and largest section.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.orchestration_statistics_builder import OrchestrationStatisticsBuilder


class OrchestrationStatisticsTests(unittest.TestCase):
    """Test suite validating statistics compilation."""

    def test_statistics_fields(self) -> None:
        """Verify built stats DTO fields are populated correctly."""
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
        recs = (rec1, rec2)
        by_sec = {"skill": (rec1,), "project": (rec2,)}
        by_cat = {"SKILL_MISSING": (rec1,), "PROJECT_MISSING": (rec2,)}
        by_pri = {"High": (rec1,), "Medium": (rec2,), "Low": ()}

        stats = OrchestrationStatisticsBuilder.build(
            recommendations=recs,
            by_section=by_sec,
            by_category=by_cat,
            by_priority=by_pri,
            execution_time_ms=1.5,
        )

        self.assertEqual(1.5, stats.execution_time_ms)
        self.assertEqual(2, stats.recommendations_processed)
        self.assertEqual(2, stats.sections)
        self.assertEqual(2, stats.categories)
        self.assertEqual(1, stats.high_priority)
        self.assertEqual(1, stats.medium_priority)
        self.assertEqual(0, stats.low_priority)
        self.assertIn(stats.largest_section, ("skill", "project"))
        self.assertIn(stats.largest_category, ("SKILL_MISSING", "PROJECT_MISSING"))
        self.assertTrue(stats.success)


if __name__ == "__main__":
    unittest.main()
