"""PrioritizationStatisticsBuilder definition.

Purpose:
    Compile PrioritizationStatistics DTOs from metrics.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.models import PrioritizationStatistics
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class PrioritizationStatisticsBuilder:
    """Builder compiling PrioritizationStatistics DTO from execution stats."""

    @staticmethod
    def build(
        recommendations: Sequence[Recommendation],
        rules: PrioritizationRules,
        execution_time_ms: float = 0.0,
        success: bool = True,
    ) -> PrioritizationStatistics:
        """Compile prioritization metrics and return a PrioritizationStatistics DTO.

        Args:
            recommendations: List of prioritized recommendations.
            rules: PrioritizationRules object to resolve priority thresholds.
            execution_time_ms: Execution duration in milliseconds.
            success: Completion status.

        Returns:
            A populated PrioritizationStatistics DTO.
        """
        processed = len(recommendations)
        high = 0
        medium = 0
        low = 0

        tot_pri = 0.0
        tot_imp = 0.0
        tot_conf = 0.0

        for rec in recommendations:
            if rules.is_high(rec.priority):
                high += 1
            elif rules.is_medium(rec.priority):
                medium += 1
            else:
                low += 1

            tot_pri += rec.priority
            tot_imp += rec.impact
            tot_conf += rec.confidence

        avg_pri = tot_pri / processed if processed > 0 else 0.0
        avg_imp = tot_imp / processed if processed > 0 else 0.0
        avg_conf = tot_conf / processed if processed > 0 else 0.0

        return PrioritizationStatistics(
            execution_time_ms=round(execution_time_ms, 4),
            recommendations_processed=processed,
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
            average_priority=round(avg_pri, 2),
            average_impact=round(avg_imp, 4),
            average_confidence=round(avg_conf, 4),
            success=success,
        )
