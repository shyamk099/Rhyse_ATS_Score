"""Unit tests for the EducationStatisticsBuilder.

Purpose:
    Verify statistical metrics dictionary creation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.education.statistics_builder import EducationStatisticsBuilder


class EducationStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating Education statistics builder outputs."""

    def test_statistics_builder_structure(self) -> None:
        stats = EducationStatisticsBuilder.build(
            matched_items=3,
            missing_items=1,
            exact_matches=2,
            higher_than_required=1,
            related_field=0,
            lower_than_required=0,
            unrelated_field=0,
            processing_time_ms=10.0,
        )

        self.assertIsInstance(stats, dict)
        self.assertEqual(3, stats["matched_items"])
        self.assertEqual(1, stats["missing_items"])
        self.assertEqual(2, stats["exact_matches"])
        self.assertEqual(1, stats["higher_than_required"])
        self.assertEqual(0, stats["related_field"])
        self.assertEqual(0, stats["lower_than_required"])
        self.assertEqual(0, stats["unrelated_field"])
        self.assertEqual(10.0, stats["processing_time_ms"])
