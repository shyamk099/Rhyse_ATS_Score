"""Tests for ExperienceRecommendationBuilder.

Purpose:
    Verify deterministic ID generation and field mappings in Experience builder.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.experience_builder import ExperienceRecommendationBuilder
from ats_engine.domain.recommendation.models import Recommendation


class ExperienceRecommendationBuilderTests(unittest.TestCase):
    """Test suite validating builder mappings."""

    def test_build_missing_experience(self) -> None:
        """Must correctly construct missing experience recommendation with clean deterministic IDs."""
        rec = ExperienceRecommendationBuilder.build_missing_recommendation("Cloud Architecture")
        self.assertEqual("EXP_MISSING_CLOUD_ARCHITECTURE", rec.recommendation_id)
        self.assertEqual("Cloud Architecture experience is missing", rec.title)
        self.assertEqual("EXPERIENCE_MISSING", rec.category)

    def test_build_partial_experience(self) -> None:
        """Must correctly construct partial experience recommendation DTO."""
        rec = ExperienceRecommendationBuilder.build_partial_recommendation("Distributed Systems")
        self.assertEqual("EXP_PARTIAL_DISTRIBUTED_SYSTEMS", rec.recommendation_id)
        self.assertEqual("Expand Distributed Systems experience", rec.title)
        self.assertEqual("EXPERIENCE_PARTIAL_MATCH", rec.category)

    def test_build_duration_gap(self) -> None:
        """Must correctly construct duration gap experience recommendation DTO."""
        rec = ExperienceRecommendationBuilder.build_duration_gap_recommendation("Microservices")
        self.assertEqual("EXP_DURATION_MICROSERVICES", rec.recommendation_id)
        self.assertEqual("Increase Microservices duration", rec.title)
        self.assertEqual("EXPERIENCE_DURATION_GAP", rec.category)


if __name__ == "__main__":
    unittest.main()
