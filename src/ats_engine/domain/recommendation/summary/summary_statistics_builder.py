"""ResumeIntelligenceStatisticsBuilder definition.

Purpose:
    Compile ResumeIntelligenceStatistics DTOs from execution metrics.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceStatistics


class ResumeIntelligenceStatisticsBuilder:
    """Builder compiling ResumeIntelligenceStatistics DTO from execution stats."""

    @staticmethod
    def build(
        execution_time_ms: float,
        sections_processed: int,
        recommendations_processed: int,
        summary_generated: bool = True,
    ) -> ResumeIntelligenceStatistics:
        """Compile summary statistics into an immutable DTO.

        Args:
            execution_time_ms: Processing duration in milliseconds.
            sections_processed: Number of sections processed.
            recommendations_processed: Number of recommendations processed.
            summary_generated: Whether the summary was successfully generated.

        Returns:
            An immutable ResumeIntelligenceStatistics DTO.
        """
        return ResumeIntelligenceStatistics(
            execution_time_ms=round(execution_time_ms, 4),
            sections_processed=sections_processed,
            recommendations_processed=recommendations_processed,
            summary_generated=summary_generated,
        )
