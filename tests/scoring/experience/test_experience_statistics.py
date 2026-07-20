"""Unit tests for the ExperienceStatisticsBuilder.

Purpose:
    Verify statistical metrics dictionary creation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.experience.statistics_builder import ExperienceStatisticsBuilder


class ExperienceStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating Experience statistics builder outputs."""

    def test_statistics_builder_structure(self) -> None:
        stats = ExperienceStatisticsBuilder.build(
            matched_items=3,
            missing_items=1,
            exact_matches=2,
            partial_matches=1,
            overqualified_matches=0,
            underqualified_matches=0,
            processing_time_ms=10.0,
        )

        self.assertIsInstance(stats, dict)
        self.assertEqual(3, stats["matched_items"])
        self.assertEqual(1, stats["missing_items"])
        self.assertEqual(2, stats["exact_matches"])
        self.assertEqual(1, stats["partial_matches"])
        self.assertEqual(0, stats["overqualified_matches"])
        self.assertEqual(0, stats["underqualified_matches"])
        self.assertEqual(10.0, stats["processing_time_ms"])
