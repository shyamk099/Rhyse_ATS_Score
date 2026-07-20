"""Unit tests for the SkillBreakdownBuilder.

Purpose:
    Verify ScoreBreakdown DTO generation and side-channel missing skills extraction.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.skill.breakdown_builder import SkillBreakdownBuilder
from tests.scoring.skill.test_skill_scorer import make_mock_result


class SkillBreakdownBuilderTests(unittest.TestCase):
    """Test suite validating breakdown builder output metrics."""

    def test_breakdown_builder(self) -> None:
        r1 = make_mock_result("M-1", "Python", "Python", missing_skills=["Java", "C++"])
        r2 = make_mock_result("M-2", "SQL", "SQL")

        breakdown = SkillBreakdownBuilder.build(
            results=[r1, r2],
            mandatory_matches=1,
            optional_matches=1,
            raw_points=3.0,
            maximum_points=40.0,
            rules_version="1.0.0",
        )

        self.assertEqual(("Python", "SQL"), breakdown.matched_items)
        self.assertEqual(("Java", "C++"), breakdown.missing_items)
        self.assertEqual(1, breakdown.classification_counts.get("mandatory"))
        self.assertEqual(1, breakdown.classification_counts.get("optional"))
        self.assertEqual(3.0, breakdown.raw_points)
        self.assertEqual(40.0, breakdown.maximum_points)
        self.assertEqual("1.0.0", breakdown.rules_version)
