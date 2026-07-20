"""Unit tests for the CertificationStatisticsBuilder.

Purpose:
    Verify statistical metrics dictionary creation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.certification.statistics_builder import CertificationStatisticsBuilder


class CertificationStatisticsBuilderTests(unittest.TestCase):
    """Test suite validating Certification statistics builder outputs."""

    def test_statistics_builder_structure(self) -> None:
        stats = CertificationStatisticsBuilder.build(
            matched_items=3,
            missing_items=1,
            exact_matches=2,
            equivalent_certifications=1,
            related_certifications=0,
            partial_matches=0,
            expired_certifications=0,
            processing_time_ms=10.0,
        )

        self.assertIsInstance(stats, dict)
        self.assertEqual(3, stats["matched_items"])
        self.assertEqual(1, stats["missing_items"])
        self.assertEqual(2, stats["exact_matches"])
        self.assertEqual(1, stats["equivalent_certifications"])
        self.assertEqual(0, stats["related_certifications"])
        self.assertEqual(0, stats["partial_matches"])
        self.assertEqual(0, stats["expired_certifications"])
        self.assertEqual(10.0, stats["processing_time_ms"])
