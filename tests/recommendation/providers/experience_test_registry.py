"""Tests for ExperienceRecommendationProvider Registry integration.

Purpose:
    Verify registry handles registering ExperienceRecommendationProvider with Skill provider.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider


class ExperienceProviderRegistryTests(unittest.TestCase):
    """Test suite validating registry integration for Experience provider."""

    def test_registry_integration_and_priority_order(self) -> None:
        """Registry must successfully register Experience provider and sort by priority order."""
        registry = RecommendationRegistry()
        skill_provider = SkillRecommendationProvider()
        exp_provider = ExperienceRecommendationProvider()

        # Register out of priority order to verify sorting
        registry.register(exp_provider)
        registry.register(skill_provider)

        self.assertEqual(2, registry.provider_count)
        self.assertTrue(registry.is_registered("SKILL"))
        self.assertTrue(registry.is_registered("EXPERIENCE"))

        ordered = registry.get_ordered_providers()
        self.assertIs(skill_provider, ordered[0])
        self.assertIs(exp_provider, ordered[1])


if __name__ == "__main__":
    unittest.main()
