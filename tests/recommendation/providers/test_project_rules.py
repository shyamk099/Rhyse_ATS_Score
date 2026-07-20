"""Tests for ProjectRecommendationRules.

Purpose:
    Verify ProjectRecommendationRules evaluations mapping to actions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.project_rules import ProjectRecommendationRules
from ats_engine.domain.recommendation.providers.base import RecommendationAction
from tests.recommendation.providers.test_project_provider import make_project_match_result


class ProjectRecommendationRulesTests(unittest.TestCase):
    """Test suite validating ProjectRecommendationRules logic."""

    def setUp(self) -> None:
        self.rules = ProjectRecommendationRules()

    def test_evaluate_missing(self) -> None:
        """Rules must resolve missing name to MISSING action."""
        self.assertEqual(RecommendationAction.MISSING, self.rules.evaluate_missing("Microservices"))
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_missing(""))

    def test_evaluate_match_partial_and_related_gaps(self) -> None:
        """Rules must resolve partial match and related/similar project classification into respective actions."""
        partial_match = make_project_match_result("M-1", "Event Driven", "PARTIAL_MATCH")
        self.assertEqual(RecommendationAction.PARTIAL, self.rules.evaluate_match(partial_match))

        related_match = make_project_match_result("M-2", "Cloud Native", "RELATED_PROJECT")
        self.assertEqual(RecommendationAction.RELATED_GAP, self.rules.evaluate_match(related_match))

        similar_match = make_project_match_result("M-3", "High Scale", "SIMILAR_PROJECT")
        self.assertEqual(RecommendationAction.RELATED_GAP, self.rules.evaluate_match(similar_match))

        exact_match = make_project_match_result("M-4", "Git", "EXACT_MATCH")
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_match(exact_match))


if __name__ == "__main__":
    unittest.main()
