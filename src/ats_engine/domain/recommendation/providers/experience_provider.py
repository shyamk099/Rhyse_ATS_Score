"""ExperienceRecommendationProvider implementation.

Purpose:
    Expose concrete BaseRecommendationProvider implementing deterministic experience recommendations.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider
from ats_engine.domain.recommendation.providers.experience_rules import ExperienceRecommendationRules, RecommendationAction
from ats_engine.domain.recommendation.providers.experience_builder import ExperienceRecommendationBuilder
from ats_engine.domain.recommendation.providers.experience_validator import ExperienceRecommendationValidator
from ats_engine.domain.recommendation.providers.experience_statistics_builder import ExperienceRecommendationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class ExperienceRecommendationProvider(BaseRecommendationProvider):
    """Provider analyzing MatchCollection and ScoreResult to suggest experience improvements."""

    PROVIDER_NAME: str = "EXPERIENCE"
    PRIORITY: int = 200

    def __init__(self, rules: ExperienceRecommendationRules | None = None) -> None:
        """Initialize the provider with optional rules."""
        self._rules = rules or ExperienceRecommendationRules()
        self._last_statistics: dict[str, Any] = {}

    def provider_name(self) -> str:
        return self.PROVIDER_NAME

    def priority(self) -> int:
        return self.PRIORITY

    @property
    def last_statistics(self) -> dict[str, Any]:
        """Return the execution stats from the last run."""
        return self._last_statistics

    def validate(self, context: RecommendationContext) -> None:
        """Validate inputs required for experience recommendations.

        Requires:
            - context.score_result.experience_score is not None.
        """
        if getattr(context.score_result, "experience_score", None) is None:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(
                "ExperienceRecommendationProvider failed validation: "
                "missing experience_score in ScoreResult."
            )

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        """Produce deterministic Experience Recommendation DTOs.

        Lifecycle:
            1. Extract missing experiences from score_result breakdown.
            2. Extract partial matches and duration gaps from match_collection.
            3. Apply rules to filter recommendations.
            4. Construct DTOs using builder.
            5. Validate output list.
            6. Return final tuple.
        """
        start_time = time.perf_counter()
        self.validate(context)

        recommendations: list[Recommendation] = []

        # 1. Missing Experiences (from ScoreResult breakdown)
        missing_experience_count = 0
        exp_score = context.score_result.experience_score
        missing_list: tuple[str, ...] = ()
        if exp_score and exp_score.breakdown:
            missing_list = exp_score.breakdown.missing_items

        for item in missing_list:
            action = self._rules.evaluate_missing(item)
            if action == RecommendationAction.MISSING:
                rec = ExperienceRecommendationBuilder.build_missing_recommendation(item)
                recommendations.append(rec)
                missing_experience_count += 1

        # 2. Matched Experiences (from MatchResults)
        partial_count = 0
        duration_gap_count = 0
        exp_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ExperienceMatcher"
        ]

        for result in exp_results:
            attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            exp_name = attrs.get("job_experience_name") or attrs.get("resume_experience_name") or result.job_feature_id

            action = self._rules.evaluate_match(result)
            if action == RecommendationAction.PARTIAL:
                rec = ExperienceRecommendationBuilder.build_partial_recommendation(exp_name)
                recommendations.append(rec)
                partial_count += 1
            elif action == RecommendationAction.DURATION_GAP:
                rec = ExperienceRecommendationBuilder.build_duration_gap_recommendation(exp_name)
                recommendations.append(rec)
                duration_gap_count += 1

        # Workload telemetry calculations
        experience_processed = len(missing_list) + len(exp_results)

        # 3. Validate generated recommendations
        ExperienceRecommendationValidator.validate(recommendations)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # 4. Compile statistics
        self._last_statistics = ExperienceRecommendationStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            experience_processed=experience_processed,
            missing_experience=missing_experience_count,
            partial_matches=partial_count,
            duration_gaps=duration_gap_count,
            recommendations_generated=len(recommendations),
            success=True,
        )

        return tuple(recommendations)
