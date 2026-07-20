"""ResumeIntelligenceSummaryEngine implementation.

Purpose:
    Final post-processor in the Book 07 pipeline.
    Consumes OrchestratedRecommendationResult and produces ResumeIntelligenceSummary.
    Does NOT generate, reprioritize, regroup, or modify recommendations.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ats_engine.domain.recommendation.post_processors.base import BasePostProcessor
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules
from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceSummary
from ats_engine.domain.recommendation.summary.summary_builder import ResumeSummaryBuilder
from ats_engine.domain.recommendation.summary.summary_validator import ResumeSummaryValidator
from ats_engine.domain.recommendation.summary.summary_statistics_builder import ResumeIntelligenceStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult


class ResumeIntelligenceSummaryEngine(BasePostProcessor):
    """Engine producing the final Resume Intelligence Summary.

    Pipeline position:
        Providers → Prioritization → Orchestration → **Summary**

    This engine:
        - Consumes only OrchestratedRecommendationResult.
        - Never reaches back to providers, prioritization, or orchestration internals.
        - Never modifies recommendation text, priorities, or IDs.
    """

    def __init__(self, rules: PrioritizationRules | None = None) -> None:
        """Initialize ResumeIntelligenceSummaryEngine with optional PrioritizationRules."""
        self._rules = rules or PrioritizationRules()

    def process(self, result: OrchestratedRecommendationResult) -> ResumeIntelligenceSummary:
        """Post-process an OrchestratedRecommendationResult into a ResumeIntelligenceSummary.

        Steps:
            1. Build summary (health, sections, top recommendations).
            2. Validate summary against orchestrated source.
            3. Compile statistics.
            4. Return immutable ResumeIntelligenceSummary.

        Args:
            result: The OrchestratedRecommendationResult from the orchestration engine.

        Returns:
            An immutable ResumeIntelligenceSummary DTO.
        """
        start_time = time.perf_counter()

        # Step 1 — Build statistics placeholder (timing filled later)
        sections_processed = len(result.recommendations_by_section)
        recommendations_processed = result.total_recommendations

        # Step 2 — Build summary
        stats_placeholder = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=0.0,
            sections_processed=sections_processed,
            recommendations_processed=recommendations_processed,
            summary_generated=True,
        )

        summary = ResumeSummaryBuilder.build(
            orchestrated=result,
            rules=self._rules,
            statistics=stats_placeholder,
        )

        # Step 3 — Validate
        ResumeSummaryValidator.validate(summary=summary, orchestrated=result)

        # Step 4 — Rebuild with actual timing
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        final_stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            sections_processed=sections_processed,
            recommendations_processed=recommendations_processed,
            summary_generated=True,
        )

        # Reconstruct with final statistics
        return ResumeIntelligenceSummary(
            overall_health=summary.overall_health,
            total_recommendations=summary.total_recommendations,
            high_priority=summary.high_priority,
            medium_priority=summary.medium_priority,
            low_priority=summary.low_priority,
            section_summaries=summary.section_summaries,
            top_recommendations=summary.top_recommendations,
            statistics=final_stats,
        )
