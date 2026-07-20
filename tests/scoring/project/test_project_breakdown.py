"""Unit tests for the ProjectBreakdownBuilder.

Purpose:
    Verify generic ScoreBreakdown DTO generation from project match results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.project.breakdown_builder import ProjectBreakdownBuilder
from tests.scoring.project.test_project_scorer import make_mock_proj_result


class ProjectBreakdownBuilderTests(unittest.TestCase):
    """Test suite validating breakdown builder output metrics."""

    def test_breakdown_builder(self) -> None:
        r1 = make_mock_proj_result("M-1", "Parser Project", "Parser Project", missing_proj=["Scoring Project"])
        r2 = make_mock_proj_result("M-2", "Crawler Project", "Crawler Project")

        breakdown = ProjectBreakdownBuilder.build(
            results=[r1, r2],
            exact_matches=1,
            similar_projects=1,
            related_projects=0,
            partial_matches=0,
            raw_points=5.5,
            maximum_points=15.0,
            rules_version="1.0.0",
        )

        self.assertEqual(("Parser Project", "Crawler Project"), breakdown.matched_items)
        self.assertEqual(("Scoring Project",), breakdown.missing_items)
        self.assertEqual(1, breakdown.classification_counts.get("exact_match"))
        self.assertEqual(1, breakdown.classification_counts.get("similar_project"))
        self.assertEqual(5.5, breakdown.raw_points)
        self.assertEqual(15.0, breakdown.maximum_points)
        self.assertEqual("1.0.0", breakdown.rules_version)
