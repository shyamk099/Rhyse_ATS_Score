"""Tests for ExperienceRecommendationRules.

Purpose:
    Verify ExperienceRecommendationRules evaluations mapping to actions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.experience_rules import ExperienceRecommendationRules, RecommendationAction
from tests.recommendation.providers.test_experience_provider import make_experience_match_result


class ExperienceRecommendationRulesTests(unittest.TestCase):
    """Test suite validating ExperienceRecommendationRules logic."""

    def setUp(self) -> None:
        self.rules = ExperienceRecommendationRules()

    def test_evaluate_missing(self) -> None:
        """Rules must resolve missing name to MISSING action."""
        self.assertEqual(RecommendationAction.MISSING, self.rules.evaluate_missing("Python"))
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_missing(""))

    def test_evaluate_match_partial_and_underqualified(self) -> None:
        """Rules must resolve partial match and underqualified classification into respective actions."""
        partial_match = make_experience_match_result("M-1", "Docker", "PARTIAL_MATCH")
        self.assertEqual(RecommendationAction.PARTIAL, self.rules.evaluate_match(partial_match))

        under_match = make_experience_match_result("M-2", "Kubernetes", "UNDERQUALIFIED")
        self.assertEqual(RecommendationAction.DURATION_GAP, self.rules.evaluate_match(under_match))

        exact_match = make_experience_match_result("M-3", "Git", "EXACT_MATCH")
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_match(exact_match))


if __name__ == "__main__":
    unittest.main()
