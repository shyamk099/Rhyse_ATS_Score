"""Tests for EducationRecommendationProvider Factory integration.

Purpose:
    Verify factory registers Skill, Experience, and Education providers.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory


class EducationProviderFactoryTests(unittest.TestCase):
    """Test suite validating factory integration with Education provider."""

    def test_factory_includes_education_provider(self) -> None:
        """create_default_recommendation_engine() must register Skill, Experience, and Education providers by default."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(5, engine.registry.provider_count)
        self.assertTrue(engine.registry.is_registered("SKILL"))
        self.assertTrue(engine.registry.is_registered("EXPERIENCE"))
        self.assertTrue(engine.registry.is_registered("EDUCATION"))


if __name__ == "__main__":
    unittest.main()
