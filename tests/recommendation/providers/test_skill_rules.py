"""Tests for SkillRecommendationRules.

Purpose:
    Verify should_recommend rules classification outputs.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.skill_rules import SkillRecommendationRules


class SkillRecommendationRulesTests(unittest.TestCase):
    """Test suite validating SkillRecommendationRules logic."""

    def setUp(self) -> None:
        self.rules = SkillRecommendationRules()

    def test_should_recommend_for_missing_and_partial(self) -> None:
        """Rules must return True for SKILL_MISSING and SKILL_PARTIAL_MATCH."""
        self.assertTrue(self.rules.should_recommend("SKILL_MISSING"))
        self.assertTrue(self.rules.should_recommend("SKILL_PARTIAL_MATCH"))

    def test_should_not_recommend_for_equivalent_or_exact(self) -> None:
        """Rules must return False for SKILL_EQUIVALENT or EXACT matches."""
        self.assertFalse(self.rules.should_recommend("SKILL_EQUIVALENT"))
        self.assertFalse(self.rules.should_recommend("EXACT"))
        self.assertFalse(self.rules.should_recommend("random_junk"))


if __name__ == "__main__":
    unittest.main()
