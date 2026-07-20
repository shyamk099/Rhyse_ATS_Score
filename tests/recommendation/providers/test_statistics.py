"""Tests for SkillRecommendationStatisticsBuilder.

Purpose:
    Verify statistics contains all timing, counts, and workloads.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.skill_statistics_builder import SkillRecommendationStatisticsBuilder


class SkillRecommendationStatisticsTests(unittest.TestCase):
    """Test suite validating skill stats builder fields."""

    def test_statistics_fields(self) -> None:
        """Verify built stats dictionary contains timing, workload, success, and count metrics."""
        stats = SkillRecommendationStatisticsBuilder.build(
            execution_time_ms=1.23,
            missing_skills=2,
            partial_skills=1,
            recommendations_generated=3,
            skills_processed=15,
            success=True,
        )
        self.assertEqual(1.23, stats["execution_time_ms"])
        self.assertEqual(2, stats["missing_skills"])
        self.assertEqual(1, stats["partial_skills"])
        self.assertEqual(3, stats["recommendations_generated"])
        self.assertEqual(15, stats["skills_processed"])
        self.assertTrue(stats["success"])


if __name__ == "__main__":
    unittest.main()
