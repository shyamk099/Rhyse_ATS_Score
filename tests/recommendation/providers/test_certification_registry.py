"""Tests for CertificationRecommendationProvider Registry integration.

Purpose:
    Verify registry handles registering CertificationRecommendationProvider with priority order.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider
from ats_engine.domain.recommendation.providers.education_provider import EducationRecommendationProvider
from ats_engine.domain.recommendation.providers.project_provider import ProjectRecommendationProvider
from ats_engine.domain.recommendation.providers.certification_provider import CertificationRecommendationProvider


class CertificationProviderRegistryTests(unittest.TestCase):
    """Test suite validating registry integration for Certification provider."""

    def test_registry_integration_and_priority_order(self) -> None:
        """Registry must successfully register Certification provider and sort by priority order."""
        registry = RecommendationRegistry()
        skill_provider = SkillRecommendationProvider()
        exp_provider = ExperienceRecommendationProvider()
        edu_provider = EducationRecommendationProvider()
        proj_provider = ProjectRecommendationProvider()
        cert_provider = CertificationRecommendationProvider()

        # Register out of priority order to verify sorting
        registry.register(cert_provider)
        registry.register(proj_provider)
        registry.register(edu_provider)
        registry.register(exp_provider)
        registry.register(skill_provider)

        self.assertEqual(5, registry.provider_count)
        self.assertTrue(registry.is_registered("SKILL"))
        self.assertTrue(registry.is_registered("EXPERIENCE"))
        self.assertTrue(registry.is_registered("EDUCATION"))
        self.assertTrue(registry.is_registered("PROJECT"))
        self.assertTrue(registry.is_registered("CERTIFICATION"))

        ordered = registry.get_ordered_providers()
        self.assertIs(skill_provider, ordered[0])
        self.assertIs(exp_provider, ordered[1])
        self.assertIs(edu_provider, ordered[2])
        self.assertIs(proj_provider, ordered[3])
        self.assertIs(cert_provider, ordered[4])


if __name__ == "__main__":
    unittest.main()
