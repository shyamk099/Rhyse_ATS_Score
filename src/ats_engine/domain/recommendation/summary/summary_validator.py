"""ResumeSummaryValidator definition.

Purpose:
    Validate the ResumeIntelligenceSummary DTO for structural integrity,
    conservation of totals, subset correctness, and uniqueness constraints.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceSummary
from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class ResumeSummaryValidator:
    """Validator verifying structural integrity of the ResumeIntelligenceSummary."""

    @staticmethod
    def validate(
        summary: ResumeIntelligenceSummary,
        orchestrated: OrchestratedRecommendationResult,
    ) -> None:
        """Validate a ResumeIntelligenceSummary against its source orchestrated result.

        Checks:
            - Total recommendations match orchestrated total.
            - Priority counts equal orchestrated priority counts.
            - Section summary totals sum to total_recommendations.
            - Top recommendations are a valid subset of the orchestrated recommendations.
            - No duplicate recommendation IDs in top_recommendations.

        Args:
            summary: The summary to validate.
            orchestrated: The source orchestrated result.

        Raises:
            RecommendationValidationError: If any validation check fails.
        """
        # Total conservation
        if summary.total_recommendations != orchestrated.total_recommendations:
            raise RecommendationValidationError(
                f"Total mismatch: summary has {summary.total_recommendations}, "
                f"orchestrated has {orchestrated.total_recommendations}"
            )

        # Priority conservation
        orch_high = len(orchestrated.recommendations_by_priority.get("High", ()))
        orch_medium = len(orchestrated.recommendations_by_priority.get("Medium", ()))
        orch_low = len(orchestrated.recommendations_by_priority.get("Low", ()))

        if summary.high_priority != orch_high:
            raise RecommendationValidationError(
                f"High priority mismatch: summary has {summary.high_priority}, "
                f"orchestrated has {orch_high}"
            )
        if summary.medium_priority != orch_medium:
            raise RecommendationValidationError(
                f"Medium priority mismatch: summary has {summary.medium_priority}, "
                f"orchestrated has {orch_medium}"
            )
        if summary.low_priority != orch_low:
            raise RecommendationValidationError(
                f"Low priority mismatch: summary has {summary.low_priority}, "
                f"orchestrated has {orch_low}"
            )

        # Priority counts must sum to total
        if summary.high_priority + summary.medium_priority + summary.low_priority != summary.total_recommendations:
            raise RecommendationValidationError(
                "Priority counts do not sum to total_recommendations"
            )

        # Section summary totals must sum to total
        section_total = sum(s.total_recommendations for s in summary.section_summaries)
        if section_total != summary.total_recommendations:
            raise RecommendationValidationError(
                f"Section summary total is {section_total}, "
                f"expected {summary.total_recommendations}"
            )

        # Top recommendations must be a subset
        main_ids = {r.recommendation_id for r in orchestrated.recommendations}
        top_ids: list[str] = []
        for rec in summary.top_recommendations:
            if rec.recommendation_id not in main_ids:
                raise RecommendationValidationError(
                    f"Top recommendation {rec.recommendation_id} not found in orchestrated list"
                )
            top_ids.append(rec.recommendation_id)

        # No duplicate IDs in top recommendations
        if len(top_ids) != len(set(top_ids)):
            raise RecommendationValidationError(
                "Duplicate recommendation ID detected in top_recommendations"
            )

        # Top recommendations must not exceed total
        if len(summary.top_recommendations) > summary.total_recommendations:
            raise RecommendationValidationError(
                f"Top recommendations count {len(summary.top_recommendations)} "
                f"exceeds total {summary.total_recommendations}"
            )
