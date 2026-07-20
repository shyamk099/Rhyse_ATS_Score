"""ProjectRecommendationStatisticsBuilder definition.

Purpose:
    Compile project recommendation provider execution statistics.
"""

from __future__ import annotations

from typing import Any


class ProjectRecommendationStatisticsBuilder:
    """Builder compiling execution metrics for ProjectRecommendationProvider."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        projects_processed: int = 0,
        missing_projects: int = 0,
        partial_matches: int = 0,
        related_gaps: int = 0,
        exact_matches: int = 0,
        equivalent_matches: int = 0,
        recommendations_generated: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Time taken to run the provider.
            projects_processed: Total number of project features processed.
            missing_projects: Number of missing project requirements.
            partial_matches: Number of partial matches.
            related_gaps: Number of related gaps.
            exact_matches: Number of exact matches.
            equivalent_matches: Number of equivalent matches.
            recommendations_generated: Number of recommendations generated.
            success: Whether the provider completed successfully.

        Returns:
            A dictionary with the statistics.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "projects_processed": projects_processed,
            "missing_projects": missing_projects,
            "partial_matches": partial_matches,
            "related_gaps": related_gaps,
            "exact_matches": exact_matches,
            "equivalent_matches": equivalent_matches,
            "recommendations_generated": recommendations_generated,
            "success": success,
        }
