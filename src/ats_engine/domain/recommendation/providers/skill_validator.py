"""SkillRecommendationValidator definition.

Purpose:
    Provide validation of generated skill recommendations.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationValidator


class SkillRecommendationValidator(BaseRecommendationValidator):
    """Validator ensuring correctness of generated Skill Recommendations."""

    @classmethod
    def validate(cls, recommendations: Sequence[Recommendation]) -> None:
        """Validate the generated recommendations.

        Delegates validation to BaseRecommendationValidator.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        cls.validate_recommendation_bounds(
            recommendations=recommendations,
            expected_section="skill",
            allowed_categories=("SKILL_MISSING", "SKILL_PARTIAL_MATCH"),
        )
