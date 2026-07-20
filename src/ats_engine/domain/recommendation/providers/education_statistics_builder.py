"""EducationRecommendationStatisticsBuilder definition.

Purpose:
    Compile education recommendation provider execution statistics.
"""

from __future__ import annotations

from typing import Any


class EducationRecommendationStatisticsBuilder:
    """Builder compiling execution metrics for EducationRecommendationProvider."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        education_processed: int = 0,
        missing_education: int = 0,
        partial_matches: int = 0,
        level_gaps: int = 0,
        exact_matches: int = 0,
        equivalent_matches: int = 0,
        recommendations_generated: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Time taken to run the provider.
            education_processed: Total number of education features processed.
            missing_education: Number of missing education requirements.
            partial_matches: Number of partial matches.
            level_gaps: Number of level gaps.
            exact_matches: Number of exact matches.
            equivalent_matches: Number of equivalent matches.
            recommendations_generated: Number of recommendations generated.
            success: Whether the provider completed successfully.

        Returns:
            A dictionary with the statistics.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "education_processed": education_processed,
            "missing_education": missing_education,
            "partial_matches": partial_matches,
            "level_gaps": level_gaps,
            "exact_matches": exact_matches,
            "equivalent_matches": equivalent_matches,
            "recommendations_generated": recommendations_generated,
            "success": success,
        }
