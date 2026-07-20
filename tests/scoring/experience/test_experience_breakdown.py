"""Unit tests for the ExperienceBreakdownBuilder.

Purpose:
    Verify generic ScoreBreakdown DTO generation from experience match results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.experience.breakdown_builder import ExperienceBreakdownBuilder
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result


class ExperienceBreakdownBuilderTests(unittest.TestCase):
    """Test suite validating breakdown builder output metrics."""

    def test_breakdown_builder(self) -> None:
        r1 = make_mock_exp_result("M-1", "Python Developer", "Python Developer", missing_exp=["Golang Developer"])
        r2 = make_mock_exp_result("M-2", "SQL Dev", "SQL Dev")

        breakdown = ExperienceBreakdownBuilder.build(
            results=[r1, r2],
            exact_matches=1,
            partial_matches=1,
            overqualified_matches=0,
            underqualified_matches=0,
            raw_points=4.5,
            maximum_points=25.0,
            rules_version="1.0.0",
        )

        self.assertEqual(("Python Developer", "SQL Dev"), breakdown.matched_items)
        self.assertEqual(("Golang Developer",), breakdown.missing_items)
        self.assertEqual(1, breakdown.classification_counts.get("exact_match"))
        self.assertEqual(1, breakdown.classification_counts.get("partial_match"))
        self.assertEqual(4.5, breakdown.raw_points)
        self.assertEqual(25.0, breakdown.maximum_points)
        self.assertEqual("1.0.0", breakdown.rules_version)
