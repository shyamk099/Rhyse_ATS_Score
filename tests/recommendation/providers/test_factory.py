"""Tests for SkillRecommendationProvider Factory integration.

Purpose:
    Verify factory configures the default engine with the SkillRecommendationProvider.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory


class SkillProviderFactoryTests(unittest.TestCase):
    """Test suite validating factory integration."""

    def test_factory_includes_skill_provider(self) -> None:
        """create_default_recommendation_engine() must register the skill provider by default."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(5, engine.registry.provider_count)
        self.assertTrue(engine.registry.is_registered("SKILL"))


if __name__ == "__main__":
    unittest.main()
