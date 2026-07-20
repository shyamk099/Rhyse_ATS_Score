"""Tests for ResumeIntelligenceStatisticsBuilder.

Purpose:
    Verify statistics builder compiles correct execution metrics.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.summary.summary_statistics_builder import ResumeIntelligenceStatisticsBuilder
from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceStatistics


class SummaryStatisticsTests(unittest.TestCase):
    """Test suite validating ResumeIntelligenceStatisticsBuilder."""

    def test_build_basic(self) -> None:
        """Basic build must populate all fields."""
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=1.2345,
            sections_processed=3,
            recommendations_processed=10,
        )
        self.assertIsInstance(stats, ResumeIntelligenceStatistics)
        self.assertEqual(1.2345, stats.execution_time_ms)
        self.assertEqual(3, stats.sections_processed)
        self.assertEqual(10, stats.recommendations_processed)
        self.assertTrue(stats.summary_generated)

    def test_build_rounding(self) -> None:
        """Execution time must be rounded to 4 decimal places."""
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=1.23456789,
            sections_processed=1,
            recommendations_processed=1,
        )
        self.assertEqual(1.2346, stats.execution_time_ms)

    def test_build_zero_values(self) -> None:
        """Zero values must be accepted."""
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=0.0,
            sections_processed=0,
            recommendations_processed=0,
        )
        self.assertEqual(0.0, stats.execution_time_ms)
        self.assertEqual(0, stats.sections_processed)
        self.assertEqual(0, stats.recommendations_processed)

    def test_build_failed_summary(self) -> None:
        """summary_generated=False must propagate."""
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=0.5,
            sections_processed=0,
            recommendations_processed=0,
            summary_generated=False,
        )
        self.assertFalse(stats.summary_generated)

    def test_immutability(self) -> None:
        """Statistics DTO must be immutable."""
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=1.0,
            sections_processed=1,
            recommendations_processed=1,
        )
        with self.assertRaises(Exception):
            stats.execution_time_ms = 99.0  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
