"""Tests for EducationRecommendationProvider Registry integration.

Purpose:
    Verify registry handles registering EducationRecommendationProvider with priority order.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider
from ats_engine.domain.recommendation.providers.education_provider import EducationRecommendationProvider


class EducationProviderRegistryTests(unittest.TestCase):
    """Test suite validating registry integration for Education provider."""

    def test_registry_integration_and_priority_order(self) -> None:
        """Registry must successfully register Education provider and sort by priority order."""
        registry = RecommendationRegistry()
        skill_provider = SkillRecommendationProvider()
        exp_provider = ExperienceRecommendationProvider()
        edu_provider = EducationRecommendationProvider()

        # Register out of priority order to verify sorting
        registry.register(edu_provider)
        registry.register(exp_provider)
        registry.register(skill_provider)

        self.assertEqual(3, registry.provider_count)
        self.assertTrue(registry.is_registered("SKILL"))
        self.assertTrue(registry.is_registered("EXPERIENCE"))
        self.assertTrue(registry.is_registered("EDUCATION"))

        ordered = registry.get_ordered_providers()
        self.assertIs(skill_provider, ordered[0])
        self.assertIs(exp_provider, ordered[1])
        self.assertIs(edu_provider, ordered[2])


if __name__ == "__main__":
    unittest.main()
