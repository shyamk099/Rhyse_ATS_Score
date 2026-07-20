"""Tests for SkillRecommendationProvider Registry integration.

Purpose:
    Verify registry handles registering SkillRecommendationProvider.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider


class SkillProviderRegistryTests(unittest.TestCase):
    """Test suite validating registry integration for Skill provider."""

    def test_registry_integration(self) -> None:
        """Registry must successfully register SkillRecommendationProvider with correct priority order."""
        registry = RecommendationRegistry()
        provider = SkillRecommendationProvider()
        registry.register(provider)

        self.assertEqual(1, registry.provider_count)
        self.assertTrue(registry.is_registered("SKILL"))
        self.assertIs(provider, registry.get_ordered_providers()[0])


if __name__ == "__main__":
    unittest.main()
