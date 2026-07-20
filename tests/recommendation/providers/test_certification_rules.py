"""Tests for CertificationRecommendationRules.

Purpose:
    Verify CertificationRecommendationRules evaluations mapping to actions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.certification_rules import CertificationRecommendationRules
from ats_engine.domain.recommendation.providers.base import RecommendationAction
from tests.recommendation.providers.test_certification_provider import make_certification_match_result


class CertificationRecommendationRulesTests(unittest.TestCase):
    """Test suite validating CertificationRecommendationRules logic."""

    def setUp(self) -> None:
        self.rules = CertificationRecommendationRules()

    def test_evaluate_missing(self) -> None:
        """Rules must resolve missing name to MISSING action."""
        self.assertEqual(RecommendationAction.MISSING, self.rules.evaluate_missing("AWS SAA"))
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_missing(""))

    def test_evaluate_match_partial_and_expired(self) -> None:
        """Rules must resolve partial match and expired certification classification into respective actions."""
        partial_match = make_certification_match_result("M-1", "Azure Administrator", "PARTIAL_MATCH")
        self.assertEqual(RecommendationAction.PARTIAL, self.rules.evaluate_match(partial_match))

        expired_match = make_certification_match_result("M-2", "PMP", "EXPIRED_CERTIFICATION")
        self.assertEqual(RecommendationAction.EXPIRED, self.rules.evaluate_match(expired_match))

        exact_match = make_certification_match_result("M-3", "AWS SAA", "EXACT_MATCH")
        self.assertEqual(RecommendationAction.NO_ACTION, self.rules.evaluate_match(exact_match))


if __name__ == "__main__":
    unittest.main()
