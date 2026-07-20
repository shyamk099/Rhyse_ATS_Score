"""ResumeSummaryBuilder definition.

Purpose:
    Assemble the ResumeIntelligenceSummary DTO from an OrchestratedRecommendationResult.
    Delegates health evaluation to ResumeHealthPolicy.
    Never modifies recommendations, priorities, or IDs.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult
from ats_engine.domain.recommendation.summary.models import (
    ResumeHealth,
    ResumeSectionSummary,
    ResumeIntelligenceSummary,
    ResumeIntelligenceStatistics,
)
from ats_engine.domain.recommendation.summary.policy import ResumeHealthPolicy
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class ResumeSummaryBuilder:
    """Builder assembling a ResumeIntelligenceSummary from orchestrated results.

    Responsibilities:
        - Delegate health evaluation to ResumeHealthPolicy.
        - Compile per-section summaries from orchestration mappings.
        - Slice the first N top recommendations (default 5).
        - Never re-sort, re-filter, or re-compute importance.
    """

    DEFAULT_TOP_N: int = 5

    @staticmethod
    def build_health(
        by_priority: Mapping[str, tuple[Recommendation, ...]],
    ) -> ResumeHealth:
        """Build ResumeHealth by delegating to ResumeHealthPolicy.

        Args:
            by_priority: Priority-tier mapping from orchestration.

        Returns:
            An immutable ResumeHealth DTO.
        """
        high_count = len(by_priority.get("High", ()))
        return ResumeHealthPolicy.evaluate(high_count)

    @staticmethod
    def build_section_summaries(
        by_section: Mapping[str, tuple[Recommendation, ...]],
        rules: PrioritizationRules,
    ) -> tuple[ResumeSectionSummary, ...]:
        """Build per-section summaries from orchestration section mapping.

        Args:
            by_section: Section mapping from orchestration.
            rules: PrioritizationRules for classifying priority tiers.

        Returns:
            Tuple of ResumeSectionSummary DTOs sorted alphabetically by section.
        """
        summaries: list[ResumeSectionSummary] = []
        for section in sorted(by_section.keys()):
            recs = by_section[section]
            high = sum(1 for r in recs if rules.is_high(r.priority))
            medium = sum(1 for r in recs if rules.is_medium(r.priority))
            low = sum(1 for r in recs if rules.is_low(r.priority))
            summaries.append(
                ResumeSectionSummary(
                    section=section,
                    total_recommendations=len(recs),
                    high_priority=high,
                    medium_priority=medium,
                    low_priority=low,
                )
            )
        return tuple(summaries)

    @staticmethod
    def build_top_recommendations(
        recommendations: Sequence[Recommendation],
        top_n: int = DEFAULT_TOP_N,
    ) -> tuple[Recommendation, ...]:
        """Slice the first N recommendations from the already-prioritized list.

        Does NOT re-sort. Does NOT re-filter. Does NOT re-compute importance.

        Args:
            recommendations: Ordered recommendation tuple from orchestration.
            top_n: Maximum number of top recommendations to include.

        Returns:
            Tuple of the first min(top_n, len(recommendations)) recommendations.
        """
        return tuple(recommendations[:top_n])

    @staticmethod
    def build(
        orchestrated: OrchestratedRecommendationResult,
        rules: PrioritizationRules,
        statistics: ResumeIntelligenceStatistics,
        top_n: int = DEFAULT_TOP_N,
    ) -> ResumeIntelligenceSummary:
        """Assemble the complete ResumeIntelligenceSummary DTO.

        Args:
            orchestrated: The OrchestratedRecommendationResult to summarize.
            rules: PrioritizationRules for classifying priority tiers.
            statistics: Pre-built ResumeIntelligenceStatistics DTO.
            top_n: Maximum number of top recommendations.

        Returns:
            An immutable ResumeIntelligenceSummary DTO.
        """
        health = ResumeSummaryBuilder.build_health(orchestrated.recommendations_by_priority)
        section_summaries = ResumeSummaryBuilder.build_section_summaries(
            orchestrated.recommendations_by_section, rules
        )
        top_recs = ResumeSummaryBuilder.build_top_recommendations(
            orchestrated.recommendations, top_n
        )

        high = len(orchestrated.recommendations_by_priority.get("High", ()))
        medium = len(orchestrated.recommendations_by_priority.get("Medium", ()))
        low = len(orchestrated.recommendations_by_priority.get("Low", ()))

        return ResumeIntelligenceSummary(
            overall_health=health,
            total_recommendations=orchestrated.total_recommendations,
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
            section_summaries=section_summaries,
            top_recommendations=top_recs,
            statistics=statistics,
        )
