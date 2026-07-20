"""CertificationRecommendationValidator definition.

Purpose:
    Provide validation of generated certification recommendations.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationValidator


class CertificationRecommendationValidator(BaseRecommendationValidator):
    """Validator ensuring correctness and scoping of generated Certification Recommendations."""

    @classmethod
    def validate(cls, recommendations: Sequence[Recommendation]) -> None:
        """Validate the generated recommendations.

        Delegates validation to BaseRecommendationValidator.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        cls.validate_recommendation_bounds(
            recommendations=recommendations,
            expected_section="certification",
            allowed_categories=("CERTIFICATION_MISSING", "CERTIFICATION_PARTIAL_MATCH", "CERTIFICATION_EXPIRED"),
        )
