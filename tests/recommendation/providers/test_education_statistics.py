"""Tests for EducationRecommendationStatisticsBuilder.

Purpose:
    Verify statistics builder compiles standard and section-specific metrics.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.education_statistics_builder import EducationRecommendationStatisticsBuilder


class EducationRecommendationStatisticsTests(unittest.TestCase):
    """Test suite validating education stats builder fields."""

    def test_statistics_fields(self) -> None:
        """Verify built stats dictionary contains timing, workload, success, and count metrics."""
        stats = EducationRecommendationStatisticsBuilder.build(
            execution_time_ms=1.23,
            education_processed=5,
            missing_education=1,
            partial_matches=2,
            level_gaps=1,
            exact_matches=1,
            equivalent_matches=0,
            recommendations_generated=4,
            success=True,
        )
        self.assertEqual(1.23, stats["execution_time_ms"])
        self.assertEqual(5, stats["education_processed"])
        self.assertEqual(1, stats["missing_education"])
        self.assertEqual(2, stats["partial_matches"])
        self.assertEqual(1, stats["level_gaps"])
        self.assertEqual(1, stats["exact_matches"])
        self.assertEqual(0, stats["equivalent_matches"])
        self.assertEqual(4, stats["recommendations_generated"])
        self.assertTrue(stats["success"])


if __name__ == "__main__":
    unittest.main()
