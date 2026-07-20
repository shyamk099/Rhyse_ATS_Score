"""Tests for EducationRecommendationRules.

Purpose:
    Verify EducationRecommendationRules evaluations mapping to actions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.education_rules import EducationRecommendationRules
from ats_engine.domain.recommendation.providers.base import RecommendationAction
from tests.recommendation.providers.test_education_provider import make_education_match_result


class EducationRecommendationRulesTests(unittest.TestCase):
    """Test suite validating EducationRecommendationRules logic."""

    def setUp(self) -> None:
        self.rules = EducationRecommendationRules()

    def test_evaluate_missing(self) -> None:
        """Rules must resolve missing name to MISSING action."""
        self.assertEqual(RecommendationAction.MISSING, self.rules.evaluate_missing("Bachelor"))
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_missing(""))

    def test_evaluate_match_partial_and_level_gap(self) -> None:
        """Rules must resolve related field and lower than required classification into respective actions."""
        partial_match = make_education_match_result("M-1", "Computer Science", "RELATED_FIELD")
        self.assertEqual(RecommendationAction.PARTIAL, self.rules.evaluate_match(partial_match))

        lower_match = make_education_match_result("M-2", "Masters", "LOWER_THAN_REQUIRED")
        self.assertEqual(RecommendationAction.LEVEL_GAP, self.rules.evaluate_match(lower_match))

        exact_match = make_education_match_result("M-3", "Bachelor", "EXACT_MATCH")
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_match(exact_match))


if __name__ == "__main__":
    unittest.main()
