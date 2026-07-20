"""Tests for EducationRecommendationValidator.

Purpose:
    Verify validator catches duplicate IDs and invalid education categories.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.education_validator import EducationRecommendationValidator
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class EducationRecommendationValidatorTests(unittest.TestCase):
    """Test suite validating EducationRecommendationValidator."""

    def test_valid_recommendations_pass(self) -> None:
        """A list of valid, unique education recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="EDU_MISSING_BACHELOR",
                section="education",
                category="EDUCATION_MISSING",
                title="Bachelor degree missing",
                description="Bachelor required.",
            ),
            Recommendation(
                recommendation_id="EDU_PARTIAL_CS",
                section="education",
                category="EDUCATION_PARTIAL_MATCH",
                title="Expand Computer Science details",
                description="CS partial.",
            ),
        ]
        EducationRecommendationValidator.validate(recs)

    def test_invalid_category_raises_validation_error(self) -> None:
        """Recommendation with an invalid category for education must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="EDU_MISSING_BACHELOR",
                section="education",
                category="SKILL_MISSING",  # invalid for education provider
                title="Bachelor is missing",
                description="Bachelor required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            EducationRecommendationValidator.validate(recs)

    def test_duplicate_ids_raise_validation_error(self) -> None:
        """Recommendations sharing duplicate ID must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="EDU_DUPE",
                section="education",
                category="EDUCATION_MISSING",
                title="Bachelor missing",
                description="Bachelor required.",
            ),
            Recommendation(
                recommendation_id="EDU_DUPE",
                section="education",
                category="EDUCATION_PARTIAL_MATCH",
                title="Expand details",
                description="CS partial.",
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            EducationRecommendationValidator.validate(recs)

    def test_invalid_section_raises_validation_error(self) -> None:
        """Recommendation with non-education section must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="EDU_MISSING_BACHELOR",
                section="skill",  # Invalid section for education validator
                category="EDUCATION_MISSING",
                title="Bachelor missing",
                description="Bachelor required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            EducationRecommendationValidator.validate(recs)


if __name__ == "__main__":
    unittest.main()
