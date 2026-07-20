"""ProjectRecommendationProvider implementation.

Purpose:
    Expose concrete BaseRecommendationProvider implementing deterministic project recommendations.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider, RecommendationAction
from ats_engine.domain.recommendation.providers.project_rules import ProjectRecommendationRules
from ats_engine.domain.recommendation.providers.project_builder import ProjectRecommendationBuilder
from ats_engine.domain.recommendation.providers.project_validator import ProjectRecommendationValidator
from ats_engine.domain.recommendation.providers.project_statistics_builder import ProjectRecommendationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class ProjectRecommendationProvider(BaseRecommendationProvider):
    """Provider analyzing MatchCollection and ScoreResult to suggest project improvements."""

    PROVIDER_NAME: str = "PROJECT"
    PRIORITY: int = 400

    def __init__(self, rules: ProjectRecommendationRules | None = None) -> None:
        """Initialize the provider with optional rules."""
        self._rules = rules or ProjectRecommendationRules()
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
        """Validate inputs required for project recommendations.

        Requires:
            - context.score_result.project_score is not None.
        """
        if getattr(context.score_result, "project_score", None) is None:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(
                "ProjectRecommendationProvider failed validation: "
                "missing project_score in ScoreResult."
            )

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        """Produce deterministic Project Recommendation DTOs.

        Lifecycle:
            1. Extract missing projects from score_result breakdown.
            2. Extract partial matches and related gaps from match_collection.
            3. Apply rules to filter recommendations.
            4. Construct DTOs using builder.
            5. Validate output list.
            6. Return final tuple.
        """
        start_time = time.perf_counter()
        self.validate(context)

        recommendations: list[Recommendation] = []

        # 1. Missing Projects (from ScoreResult breakdown)
        missing_count = 0
        proj_score = context.score_result.project_score
        missing_list: tuple[str, ...] = ()
        if proj_score and proj_score.breakdown:
            missing_list = proj_score.breakdown.missing_items

        for item in missing_list:
            action = self._rules.evaluate_missing(item)
            if action == RecommendationAction.MISSING:
                rec = ProjectRecommendationBuilder.build_missing_recommendation(item)
                recommendations.append(rec)
                missing_count += 1

        # 2. Matched Projects (from MatchResults)
        partial_count = 0
        related_gap_count = 0
        exact_matches = 0
        equivalent_matches = 0

        proj_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ProjectMatcher"
        ]

        for result in proj_results:
            attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            proj_name = attrs.get("job_project_name") or attrs.get("resume_project_name") or result.job_feature_id

            action = self._rules.evaluate_match(result)
            if action == RecommendationAction.PARTIAL:
                rec = ProjectRecommendationBuilder.build_partial_recommendation(proj_name)
                recommendations.append(rec)
                partial_count += 1
            elif action == RecommendationAction.RELATED_GAP:
                rec = ProjectRecommendationBuilder.build_related_gap_recommendation(proj_name)
                recommendations.append(rec)
                related_gap_count += 1
            else:
                val = (attrs.get("match_type") or attrs.get("classification") or "").upper()
                if val in ("EXACT_MATCH", "EXACT"):
                    exact_matches += 1
                else:
                    equivalent_matches += 1

        # Workload telemetry calculations
        projects_processed = len(missing_list) + len(proj_results)

        # 3. Validate generated recommendations
        ProjectRecommendationValidator.validate(recommendations)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # 4. Compile statistics
        self._last_statistics = ProjectRecommendationStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            projects_processed=projects_processed,
            missing_projects=missing_count,
            partial_matches=partial_count,
            related_gaps=related_gap_count,
            exact_matches=exact_matches,
            equivalent_matches=equivalent_matches,
            recommendations_generated=len(recommendations),
            success=True,
        )

        return tuple(recommendations)
