"""Unit tests for the SkillStatisticsBuilder.

Purpose:
    Verify statistical metrics dictionary creation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.skill.statistics_builder import SkillStatisticsBuilder


class SkillStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating Skill statistics builder outputs."""

    def test_statistics_builder_structure(self) -> None:
        stats = SkillStatisticsBuilder.build(
            matched_items=5,
            missing_items=3,
            mandatory_matches=4,
            optional_matches=1,
            raw_points=9.0,
            total_items=8,
            processing_time_ms=5.0,
        )

        self.assertIsInstance(stats, dict)
        self.assertEqual(5, stats["matched_items"])
        self.assertEqual(3, stats["missing_items"])
        self.assertEqual(4, stats["mandatory_matches"])
        self.assertEqual(1, stats["optional_matches"])
        self.assertEqual(9.0, stats["raw_points"])
        self.assertEqual(8, stats["total_items"])
        self.assertEqual(5.0, stats["processing_time_ms"])
