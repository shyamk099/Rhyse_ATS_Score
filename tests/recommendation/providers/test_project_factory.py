"""Tests for ProjectRecommendationProvider Factory integration.

Purpose:
    Verify factory registers Skill, Experience, Education, and Project providers.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory


class ProjectProviderFactoryTests(unittest.TestCase):
    """Test suite validating factory integration with Project provider."""

    def test_factory_includes_project_provider(self) -> None:
        """create_default_recommendation_engine() must register Skill, Experience, Education, and Project providers by default."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(5, engine.registry.provider_count)
        self.assertTrue(engine.registry.is_registered("SKILL"))
        self.assertTrue(engine.registry.is_registered("EXPERIENCE"))
        self.assertTrue(engine.registry.is_registered("EDUCATION"))
        self.assertTrue(engine.registry.is_registered("PROJECT"))


if __name__ == "__main__":
    unittest.main()
