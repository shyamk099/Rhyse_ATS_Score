"""ExperienceRecommendationStatisticsBuilder definition.

Purpose:
    Compile experience recommendation provider execution statistics.
"""

from __future__ import annotations

from typing import Any


class ExperienceRecommendationStatisticsBuilder:
    """Builder compiling execution metrics for ExperienceRecommendationProvider."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        experience_processed: int = 0,
        missing_experience: int = 0,
        partial_matches: int = 0,
        duration_gaps: int = 0,
        recommendations_generated: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Time taken to run the provider.
            experience_processed: Total number of experiences processed.
            missing_experience: Number of missing experiences detected.
            partial_matches: Number of partially matched experiences detected.
            duration_gaps: Number of duration gaps detected.
            recommendations_generated: Number of recommendations generated.
            success: Whether the provider completed successfully.

        Returns:
            A dictionary with the statistics.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "experience_processed": experience_processed,
            "missing_experience": missing_experience,
            "partial_matches": partial_matches,
            "duration_gaps": duration_gaps,
            "recommendations_generated": recommendations_generated,
            "success": success,
        }
