"""ProjectRecommendationValidator definition.

Purpose:
    Provide validation of generated project recommendations.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationValidator


class ProjectRecommendationValidator(BaseRecommendationValidator):
    """Validator ensuring correctness and scoping of generated Project Recommendations."""

    @classmethod
    def validate(cls, recommendations: Sequence[Recommendation]) -> None:
        """Validate the generated recommendations.

        Delegates validation to BaseRecommendationValidator.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        cls.validate_recommendation_bounds(
            recommendations=recommendations,
            expected_section="project",
            allowed_categories=("PROJECT_MISSING", "PROJECT_PARTIAL_MATCH", "PROJECT_RELATED_GAP"),
        )
