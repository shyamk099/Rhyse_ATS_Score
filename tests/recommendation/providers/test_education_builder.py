"""Tests for EducationRecommendationBuilder.

Purpose:
    Verify deterministic ID generation and field mappings in Education builder.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.education_builder import EducationRecommendationBuilder
from ats_engine.domain.recommendation.models import Recommendation


class EducationRecommendationBuilderTests(unittest.TestCase):
    """Test suite validating builder mappings."""

    def test_build_missing_education(self) -> None:
        """Must correctly construct missing education recommendation with clean deterministic IDs."""
        rec = EducationRecommendationBuilder.build_missing_recommendation("Bachelor")
        self.assertEqual("EDU_MISSING_BACHELOR", rec.recommendation_id)
        self.assertEqual("Bachelor degree is missing", rec.title)
        self.assertEqual("EDUCATION_MISSING", rec.category)

    def test_build_partial_education(self) -> None:
        """Must correctly construct partial education recommendation DTO."""
        rec = EducationRecommendationBuilder.build_partial_recommendation("Computer Science")
        self.assertEqual("EDU_PARTIAL_COMPUTER_SCIENCE", rec.recommendation_id)
        self.assertEqual("Expand Computer Science education details", rec.title)
        self.assertEqual("EDUCATION_PARTIAL_MATCH", rec.category)

    def test_build_level_gap(self) -> None:
        """Must correctly construct level gap education recommendation DTO."""
        rec = EducationRecommendationBuilder.build_level_gap_recommendation("Masters")
        self.assertEqual("EDU_LEVEL_GAP_MASTERS", rec.recommendation_id)
        self.assertEqual("Upgrade to Masters qualification", rec.title)
        self.assertEqual("EDUCATION_LEVEL_GAP", rec.category)


if __name__ == "__main__":
    unittest.main()
