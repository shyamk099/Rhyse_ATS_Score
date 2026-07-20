"""Unit tests for the ProjectStatisticsBuilder.

Purpose:
    Verify statistical metrics dictionary creation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.project.statistics_builder import ProjectStatisticsBuilder


class ProjectStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating Project statistics builder outputs."""

    def test_statistics_builder_structure(self) -> None:
        stats = ProjectStatisticsBuilder.build(
            matched_items=3,
            missing_items=1,
            exact_matches=2,
            similar_projects=1,
            related_projects=0,
            partial_matches=0,
            processing_time_ms=10.0,
        )

        self.assertIsInstance(stats, dict)
        self.assertEqual(3, stats["matched_items"])
        self.assertEqual(1, stats["missing_items"])
        self.assertEqual(2, stats["exact_matches"])
        self.assertEqual(1, stats["similar_projects"])
        self.assertEqual(0, stats["related_projects"])
        self.assertEqual(0, stats["partial_matches"])
        self.assertEqual(10.0, stats["processing_time_ms"])
