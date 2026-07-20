"""EducationRecommendationValidator definition.

Purpose:
    Provide validation of generated education recommendations.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationValidator


class EducationRecommendationValidator(BaseRecommendationValidator):
    """Validator ensuring correctness and scoping of generated Education Recommendations."""

    @classmethod
    def validate(cls, recommendations: Sequence[Recommendation]) -> None:
        """Validate the generated recommendations.

        Delegates validation to BaseRecommendationValidator.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        cls.validate_recommendation_bounds(
            recommendations=recommendations,
            expected_section="education",
            allowed_categories=("EDUCATION_MISSING", "EDUCATION_PARTIAL_MATCH", "EDUCATION_LEVEL_GAP"),
        )
