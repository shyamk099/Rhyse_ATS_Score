"""Tests for ExperienceRecommendationProvider Factory integration.

Purpose:
    Verify factory registers both Skill and Experience providers.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory


class ExperienceProviderFactoryTests(unittest.TestCase):
    """Test suite validating factory integration with Experience provider."""

    def test_factory_includes_experience_provider(self) -> None:
        """create_default_recommendation_engine() must register both Skill and Experience providers by default."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(5, engine.registry.provider_count)
        self.assertTrue(engine.registry.is_registered("SKILL"))
        self.assertTrue(engine.registry.is_registered("EXPERIENCE"))


if __name__ == "__main__":
    unittest.main()
