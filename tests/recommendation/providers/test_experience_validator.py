"""Tests for ExperienceRecommendationValidator.

Purpose:
    Verify validator catches duplicate IDs and invalid experience categories.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.experience_validator import ExperienceRecommendationValidator
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class ExperienceRecommendationValidatorTests(unittest.TestCase):
    """Test suite validating ExperienceRecommendationValidator."""

    def test_valid_recommendations_pass(self) -> None:
        """A list of valid, unique experience recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="EXP_MISSING_DOCKER",
                section="experience",
                category="EXPERIENCE_MISSING",
                title="Docker experience is missing",
                description="Docker required.",
            ),
            Recommendation(
                recommendation_id="EXP_PARTIAL_GIT",
                section="experience",
                category="EXPERIENCE_PARTIAL_MATCH",
                title="Expand Git experience",
                description="Git partial.",
            ),
        ]
        ExperienceRecommendationValidator.validate(recs)

    def test_invalid_category_raises_validation_error(self) -> None:
        """Recommendation with an invalid category for experience must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="EXP_MISSING_DOCKER",
                section="experience",
                category="SKILL_MISSING",  # invalid for experience provider
                title="Docker is missing",
                description="Docker required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            ExperienceRecommendationValidator.validate(recs)

    def test_duplicate_ids_raise_validation_error(self) -> None:
        """Recommendations sharing duplicate ID must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="EXP_DUPE",
                section="experience",
                category="EXPERIENCE_MISSING",
                title="Docker experience missing",
                description="Docker required.",
            ),
            Recommendation(
                recommendation_id="EXP_DUPE",
                section="experience",
                category="EXPERIENCE_PARTIAL_MATCH",
                title="Expand Git experience",
                description="Git partial.",
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            ExperienceRecommendationValidator.validate(recs)


if __name__ == "__main__":
    unittest.main()
