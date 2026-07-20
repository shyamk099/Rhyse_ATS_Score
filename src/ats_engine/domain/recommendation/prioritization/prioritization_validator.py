"""PrioritizationValidator definition.

Purpose:
    Enforce validation constraints on prioritized recommendation results.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class PrioritizationValidator:
    """Validator verifying correctness, ranges, and deterministic ordering of prioritized DTOs."""

    @staticmethod
    def validate(recommendations: Sequence[Recommendation]) -> None:
        """Validate prioritized DTO fields and sorted ordering.

        Checks:
            - Priority >= 0.
            - Impact between 0.0 and 1.0 (or 100.0 if scaling differs, but rules assign 0.0-1.0).
              Wait, the Recommendation DTO allows impact up to 100.0, but rules use 0.0-1.0. Let's support both.
            - Confidence between 0.0 and 1.0.
            - Duplicate IDs are caught.
            - Ordered correctly: priority descending, impact descending, ID ascending.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        seen_ids: set[str] = set()
        prev_pri: int = 999999
        prev_imp: float = 999999.0
        prev_id: str = ""

        for rec in recommendations:
            if rec.priority < 0:
                raise RecommendationValidationError("Priority must be non-negative.")
            if not (0.0 <= rec.impact <= 100.0):
                raise RecommendationValidationError("Impact must be between 0.0 and 100.0.")
            if not (0.0 <= rec.confidence <= 1.0):
                raise RecommendationValidationError("Confidence must be between 0.0 and 1.0.")

            if rec.recommendation_id in seen_ids:
                raise RecommendationValidationError(
                    f"Duplicate recommendation ID detected: {rec.recommendation_id}"
                )
            seen_ids.add(rec.recommendation_id)

            # Assert sorting order: priority DESC, impact DESC, ID ASC
            if rec.priority > prev_pri:
                raise RecommendationValidationError("Recommendations not sorted by priority descending.")
            elif rec.priority == prev_pri:
                if rec.impact > prev_imp:
                    raise RecommendationValidationError("Recommendations not sorted by impact descending.")
                elif rec.impact == prev_imp:
                    if rec.recommendation_id < prev_id:
                        raise RecommendationValidationError("Recommendations not sorted by ID ascending tie-breaker.")

            prev_pri = rec.priority
            prev_imp = rec.impact
            prev_id = rec.recommendation_id
