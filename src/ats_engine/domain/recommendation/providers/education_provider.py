"""EducationRecommendationProvider implementation.

Purpose:
    Expose concrete BaseRecommendationProvider implementing deterministic education recommendations.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider, RecommendationAction
from ats_engine.domain.recommendation.providers.education_rules import EducationRecommendationRules
from ats_engine.domain.recommendation.providers.education_builder import EducationRecommendationBuilder
from ats_engine.domain.recommendation.providers.education_validator import EducationRecommendationValidator
from ats_engine.domain.recommendation.providers.education_statistics_builder import EducationRecommendationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class EducationRecommendationProvider(BaseRecommendationProvider):
    """Provider analyzing MatchCollection and ScoreResult to suggest education improvements."""

    PROVIDER_NAME: str = "EDUCATION"
    PRIORITY: int = 300

    def __init__(self, rules: EducationRecommendationRules | None = None) -> None:
        """Initialize the provider with optional rules."""
        self._rules = rules or EducationRecommendationRules()
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
        """Validate inputs required for education recommendations.

        Requires:
            - context.score_result.education_score is not None.
        """
        if getattr(context.score_result, "education_score", None) is None:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(
                "EducationRecommendationProvider failed validation: "
                "missing education_score in ScoreResult."
            )

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        """Produce deterministic Education Recommendation DTOs.

        Lifecycle:
            1. Extract missing education from score_result breakdown.
            2. Extract partial matches and level gaps from match_collection.
            3. Apply rules to filter recommendations.
            4. Construct DTOs using builder.
            5. Validate output list.
            6. Return final tuple.
        """
        start_time = time.perf_counter()
        self.validate(context)

        recommendations: list[Recommendation] = []

        # 1. Missing Education (from ScoreResult breakdown)
        missing_count = 0
        edu_score = context.score_result.education_score
        missing_list: tuple[str, ...] = ()
        if edu_score and edu_score.breakdown:
            missing_list = edu_score.breakdown.missing_items

        for item in missing_list:
            action = self._rules.evaluate_missing(item)
            if action == RecommendationAction.MISSING:
                rec = EducationRecommendationBuilder.build_missing_recommendation(item)
                recommendations.append(rec)
                missing_count += 1

        # 2. Matched Education (from MatchResults)
        partial_count = 0
        level_gap_count = 0
        exact_matches = 0
        equivalent_matches = 0

        edu_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "EducationMatcher"
        ]

        for result in edu_results:
            attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            edu_name = attrs.get("job_education_name") or attrs.get("resume_education_name") or result.job_feature_id

            action = self._rules.evaluate_match(result)
            if action == RecommendationAction.PARTIAL:
                rec = EducationRecommendationBuilder.build_partial_recommendation(edu_name)
                recommendations.append(rec)
                partial_count += 1
            elif action == RecommendationAction.LEVEL_GAP:
                rec = EducationRecommendationBuilder.build_level_gap_recommendation(edu_name)
                recommendations.append(rec)
                level_gap_count += 1
            else:
                val = (attrs.get("match_type") or attrs.get("classification") or "").upper()
                if val in ("EXACT_MATCH", "EXACT", "HIGHER_THAN_REQUIRED"):
                    exact_matches += 1
                else:
                    equivalent_matches += 1

        # Workload telemetry calculations
        education_processed = len(missing_list) + len(edu_results)

        # 3. Validate generated recommendations
        EducationRecommendationValidator.validate(recommendations)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # 4. Compile statistics
        self._last_statistics = EducationRecommendationStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            education_processed=education_processed,
            missing_education=missing_count,
            partial_matches=partial_count,
            level_gaps=level_gap_count,
            exact_matches=exact_matches,
            equivalent_matches=equivalent_matches,
            recommendations_generated=len(recommendations),
            success=True,
        )

        return tuple(recommendations)
