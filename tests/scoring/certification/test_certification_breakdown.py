"""Unit tests for the CertificationBreakdownBuilder.

Purpose:
    Verify generic ScoreBreakdown DTO generation from certification match results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.certification.breakdown_builder import CertificationBreakdownBuilder
from tests.scoring.certification.test_certification_scorer import make_mock_cert_result


class CertificationBreakdownBuilderTests(unittest.TestCase):
    """Test suite validating breakdown builder output metrics."""

    def test_breakdown_builder(self) -> None:
        r1 = make_mock_cert_result("M-1", "PMP", "PMP", missing_cert=["ITIL"])
        r2 = make_mock_cert_result("M-2", "AWS Cloud", "AWS Cloud")

        breakdown = CertificationBreakdownBuilder.build(
            results=[r1, r2],
            exact_matches=1,
            equivalent_certifications=1,
            related_certifications=0,
            partial_matches=0,
            expired_certifications=0,
            raw_points=5.5,
            maximum_points=10.0,
            rules_version="1.0.0",
        )

        self.assertEqual(("PMP", "AWS Cloud"), breakdown.matched_items)
        self.assertEqual(("ITIL",), breakdown.missing_items)
        self.assertEqual(1, breakdown.classification_counts.get("exact_match"))
        self.assertEqual(1, breakdown.classification_counts.get("equivalent_certification"))
        self.assertEqual(5.5, breakdown.raw_points)
        self.assertEqual(10.0, breakdown.maximum_points)
        self.assertEqual("1.0.0", breakdown.rules_version)
