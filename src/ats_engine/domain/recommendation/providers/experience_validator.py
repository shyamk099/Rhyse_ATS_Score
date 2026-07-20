"""ExperienceRecommendationValidator definition.

Purpose:
    Provide validation of generated experience recommendations.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationValidator


class ExperienceRecommendationValidator(BaseRecommendationValidator):
    """Validator ensuring correctness of generated Experience Recommendations."""

    @classmethod
    def validate(cls, recommendations: Sequence[Recommendation]) -> None:
        """Validate the generated recommendations.

        Delegates validation to BaseRecommendationValidator.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        cls.validate_recommendation_bounds(
            recommendations=recommendations,
            expected_section="experience",
            allowed_categories=("EXPERIENCE_MISSING", "EXPERIENCE_PARTIAL_MATCH", "EXPERIENCE_DURATION_GAP"),
        )
