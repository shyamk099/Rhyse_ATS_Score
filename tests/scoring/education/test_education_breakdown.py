"""Unit tests for the EducationBreakdownBuilder.

Purpose:
    Verify generic ScoreBreakdown DTO generation from education match results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.education.breakdown_builder import EducationBreakdownBuilder
from tests.scoring.education.test_education_scorer import make_mock_edu_result


class EducationBreakdownBuilderTests(unittest.TestCase):
    """Test suite validating breakdown builder output metrics."""

    def test_breakdown_builder(self) -> None:
        r1 = make_mock_edu_result("M-1", "BSc Computer Science", "BSc Computer Science", missing_edu=["MSc Comp Sci"])
        r2 = make_mock_edu_result("M-2", "BSc Math", "BSc Math")

        breakdown = EducationBreakdownBuilder.build(
            results=[r1, r2],
            exact_matches=1,
            higher_than_required=0,
            related_field=1,
            lower_than_required=0,
            unrelated_field=0,
            raw_points=6.5,
            maximum_points=15.0,
            rules_version="1.0.0",
        )

        self.assertEqual(("BSc Computer Science", "BSc Math"), breakdown.matched_items)
        self.assertEqual(("MSc Comp Sci",), breakdown.missing_items)
        self.assertEqual(1, breakdown.classification_counts.get("exact_match"))
        self.assertEqual(1, breakdown.classification_counts.get("related_field"))
        self.assertEqual(6.5, breakdown.raw_points)
        self.assertEqual(15.0, breakdown.maximum_points)
        self.assertEqual("1.0.0", breakdown.rules_version)
