"""PrioritizationEngine implementation.

Purpose:
    Expose prioritization post-processing pipeline stage.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ats_engine.domain.recommendation.post_processors.base import BasePostProcessor
from ats_engine.domain.recommendation.prioritization.models import PrioritizedRecommendationResult
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules
from ats_engine.domain.recommendation.prioritization.prioritization_builder import PrioritizationBuilder
from ats_engine.domain.recommendation.prioritization.prioritization_validator import PrioritizationValidator
from ats_engine.domain.recommendation.prioritization.prioritization_statistics_builder import PrioritizationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import RecommendationResult


class PrioritizationEngine(BasePostProcessor):
    """Engine orchestrating the recommendation prioritization pipeline."""

    def __init__(self, rules: PrioritizationRules | None = None) -> None:
        """Initialize PrioritizationEngine with optional custom rules."""
        self._rules = rules or PrioritizationRules()

    @property
    def rules(self) -> PrioritizationRules:
        """Return the active prioritization rules."""
        return self._rules

    def process(self, result: RecommendationResult) -> PrioritizedRecommendationResult:
        """Post-process a RecommendationResult.

        Updates priority, impact, and confidence, sorts them, compiles statistics,
        and returns a PrioritizedRecommendationResult DTO.
        """
        start_time = time.perf_counter()

        # Step 1 — Map and sort recommendations
        prioritized = PrioritizationBuilder.prioritize_and_sort(
            recommendations=result.recommendations,
            rules=self._rules,
        )

        # Step 2 — Validate results
        PrioritizationValidator.validate(prioritized)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 3 — Compile statistics
        stats = PrioritizationStatisticsBuilder.build(
            recommendations=prioritized,
            rules=self._rules,
            execution_time_ms=duration_ms,
            success=True,
        )

        # Count priorities
        high = stats.high_priority
        medium = stats.medium_priority
        low = stats.low_priority

        return PrioritizedRecommendationResult(
            recommendations=prioritized,
            statistics=stats,
            total_recommendations=len(prioritized),
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
        )
