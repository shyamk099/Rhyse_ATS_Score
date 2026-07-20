"""Tests for RecommendationStatisticsBuilder.

Purpose:
    Verify statistics builder produces correct keys, types, and rounding.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.statistics_builder import RecommendationStatisticsBuilder


class RecommendationStatisticsTests(unittest.TestCase):
    """Test suite validating statistics builder."""

    def test_statistics_builder_correct_fields(self) -> None:
        """Verify built stats dict contains all expected keys and correctly rounded numbers."""
        stats = RecommendationStatisticsBuilder.build(
            execution_time_ms=12.34567,
            providers_executed=("SKILL", "EXPERIENCE"),
            recommendations_generated=2,
            success=True,
        )
        self.assertEqual(12.3457, stats["execution_time_ms"])
        self.assertEqual(("SKILL", "EXPERIENCE"), stats["providers_executed"])
        self.assertEqual(2, stats["recommendations_generated"])
        self.assertTrue(stats["success"])


if __name__ == "__main__":
    unittest.main()
