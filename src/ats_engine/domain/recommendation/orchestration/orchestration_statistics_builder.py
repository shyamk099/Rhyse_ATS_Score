"""OrchestrationStatisticsBuilder definition.

Purpose:
    Compile OrchestrationStatistics DTOs from metrics.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import OrchestrationStatistics


class OrchestrationStatisticsBuilder:
    """Builder compiling OrchestrationStatistics DTO from execution stats."""

    @staticmethod
    def build(
        recommendations: Sequence[Recommendation],
        by_section: Mapping[str, tuple[Recommendation, ...]],
        by_category: Mapping[str, tuple[Recommendation, ...]],
        by_priority: Mapping[str, tuple[Recommendation, ...]],
        execution_time_ms: float = 0.0,
        success: bool = True,
    ) -> OrchestrationStatistics:
        """Compile orchestration metrics and return an OrchestrationStatistics DTO.

        Args:
            recommendations: List of sorted recommendations.
            by_section: Section mapping.
            by_category: Category mapping.
            by_priority: Priority mapping.
            execution_time_ms: Processing duration.
            success: Execution status.

        Returns:
            A populated OrchestrationStatistics DTO.
        """
        processed = len(recommendations)

        # Largest section
        largest_section = ""
        max_sec_len = -1
        for sec, items in by_section.items():
            if len(items) > max_sec_len:
                max_sec_len = len(items)
                largest_section = sec

        # Largest category
        largest_category = ""
        max_cat_len = -1
        for cat, items in by_category.items():
            if len(items) > max_cat_len:
                max_cat_len = len(items)
                largest_category = cat

        high = len(by_priority.get("High", ()))
        medium = len(by_priority.get("Medium", ()))
        low = len(by_priority.get("Low", ()))

        return OrchestrationStatistics(
            execution_time_ms=round(execution_time_ms, 4),
            recommendations_processed=processed,
            sections=len(by_section),
            categories=len(by_category),
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
            largest_section=largest_section,
            largest_category=largest_category,
            success=success,
        )
