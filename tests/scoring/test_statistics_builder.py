"""Unit tests for the ScoreStatisticsBuilder.

Purpose:
    Verify statistics compiling and correct DTO serialization fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.common.statistics_builder import ScoreStatisticsBuilder
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics


class ScoreStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating ScoreStatisticsBuilder behaviors."""

    def test_statistics_builder_populates_correct_dto(self) -> None:
        stats = ScoreStatisticsBuilder.build(
            total_sections=5,
            registered_scorers=("SKILL", "EXPERIENCE"),
            executed_scorers=("SKILL",),
            skipped_scorers=("EXPERIENCE",),
            failed_scorers=("EDUCATION",),
            warnings=("Dummy warning",),
            validation_errors=("Dummy error",),
            processing_time_ms=12.5,
        )

        self.assertIsInstance(stats, ScoreStatistics)
        self.assertEqual(5, stats.total_sections)
        self.assertEqual(("SKILL", "EXPERIENCE"), stats.registered_scorers)
        self.assertEqual(("SKILL",), stats.executed_scorers)
        self.assertEqual(("EXPERIENCE",), stats.skipped_scorers)
        self.assertEqual(("EDUCATION",), stats.failed_scorers)
        self.assertEqual(("Dummy warning",), stats.warnings)
        self.assertEqual(("Dummy error",), stats.validation_errors)
        self.assertEqual(12.5, stats.processing_time_ms)
