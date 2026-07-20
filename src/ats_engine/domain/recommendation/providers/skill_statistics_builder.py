"""SkillRecommendationStatisticsBuilder definition.

Purpose:
    Compile skill recommendation provider execution statistics.
"""

from __future__ import annotations

from typing import Any


class SkillRecommendationStatisticsBuilder:
    """Builder compiling execution metrics for SkillRecommendationProvider."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        missing_skills: int = 0,
        partial_skills: int = 0,
        recommendations_generated: int = 0,
        skills_processed: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Time taken to run the provider.
            missing_skills: Number of missing skills detected.
            partial_skills: Number of partially matched skills detected.
            recommendations_generated: Number of recommendations generated.
            skills_processed: Total number of skills processed (workload metric).
            success: Whether the provider completed successfully.

        Returns:
            A dictionary with the statistics.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "missing_skills": missing_skills,
            "partial_skills": partial_skills,
            "recommendations_generated": recommendations_generated,
            "skills_processed": skills_processed,
            "success": success,
        }
