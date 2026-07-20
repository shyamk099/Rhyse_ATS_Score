"""RecommendationOrchestrationEngine implementation.

Purpose:
    Expose recommendation grouping and packaging pipeline stage.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ats_engine.domain.recommendation.post_processors.base import BasePostProcessor
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules
from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult
from ats_engine.domain.recommendation.orchestration.orchestration_builder import RecommendationOrchestrationBuilder
from ats_engine.domain.recommendation.orchestration.orchestration_validator import RecommendationOrchestrationValidator
from ats_engine.domain.recommendation.orchestration.orchestration_statistics_builder import OrchestrationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult


class RecommendationOrchestrationEngine(BasePostProcessor):
    """Engine orchestrating the recommendation grouping and packaging pipeline."""

    def __init__(self, rules: PrioritizationRules | None = None) -> None:
        """Initialize RecommendationOrchestrationEngine with optional PrioritizationRules."""
        self._rules = rules or PrioritizationRules()

    def process(self, result: PrioritizedRecommendationResult) -> OrchestratedRecommendationResult:
        """Post-process a PrioritizedRecommendationResult.

        Groups recommendations by section, category, and priority tier, validates
        mappings, compiles statistics, and returns an OrchestratedRecommendationResult DTO.
        """
        start_time = time.perf_counter()

        recs = result.recommendations

        # Step 1 — Grouping
        by_section = RecommendationOrchestrationBuilder.build_section_groups(recs)
        by_category = RecommendationOrchestrationBuilder.build_category_groups(recs)
        by_priority = RecommendationOrchestrationBuilder.build_priority_groups(recs, self._rules)

        # Step 2 — Validation
        RecommendationOrchestrationValidator.validate(
            recommendations=recs,
            by_section=by_section,
            by_category=by_category,
            by_priority=by_priority,
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 3 — Compile statistics
        stats = OrchestrationStatisticsBuilder.build(
            recommendations=recs,
            by_section=by_section,
            by_category=by_category,
            by_priority=by_priority,
            execution_time_ms=duration_ms,
            success=True,
        )

        return OrchestratedRecommendationResult(
            recommendations=recs,
            grouped_recommendations=by_category,
            recommendations_by_section=by_section,
            recommendations_by_priority=by_priority,
            statistics=stats,
            total_recommendations=len(recs),
        )
