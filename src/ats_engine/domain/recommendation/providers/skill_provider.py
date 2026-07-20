"""SkillRecommendationProvider implementation.

Purpose:
    Expose concrete BaseRecommendationProvider implementing deterministic skill recommendation rules.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider
from ats_engine.domain.recommendation.providers.skill_rules import SkillRecommendationRules
from ats_engine.domain.recommendation.providers.skill_builder import SkillRecommendationBuilder
from ats_engine.domain.recommendation.providers.skill_validator import SkillRecommendationValidator
from ats_engine.domain.recommendation.providers.skill_statistics_builder import SkillRecommendationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class SkillRecommendationProvider(BaseRecommendationProvider):
    """Provider analyzing MatchCollection and ScoreResult to suggest missing/partial skills."""

    PROVIDER_NAME: str = "SKILL"
    PRIORITY: int = 100

    def __init__(self, rules: SkillRecommendationRules | None = None) -> None:
        """Initialize the provider with optional rules."""
        self._rules = rules or SkillRecommendationRules()
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
        """Validate inputs required for skill recommendations.

        Requires:
            - context.score_result.skill_score is not None.
        """
        if getattr(context.score_result, "skill_score", None) is None:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(
                "SkillRecommendationProvider failed validation: "
                "missing skill_score in ScoreResult."
            )

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        """Produce deterministic Skill Recommendation DTOs.

        Lifecycle:
            1. Extract missing skills from score_result breakdown.
            2. Extract partial matches from match_collection results based on custom attributes.
            3. Apply rules to filter recommendations.
            4. Construct DTOs using builder.
            5. Validate output list.
            6. Return final tuple.
        """
        start_time = time.perf_counter()
        self.validate(context)

        recommendations: list[Recommendation] = []
        index = 1

        # 1. Missing Skills (from ScoreResult breakdown)
        missing_skills = []
        skill_score = context.score_result.skill_score
        if skill_score and skill_score.breakdown:
            missing_skills = list(skill_score.breakdown.missing_items)

        for skill in missing_skills:
            if self._rules.should_recommend("SKILL_MISSING"):
                rec = SkillRecommendationBuilder.build_missing_recommendation(skill, index)
                recommendations.append(rec)
                index += 1

        # 2. Partially Matched Skills (from MatchResults)
        partial_skills = []
        skill_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "SkillMatcher"
        ]

        for result in skill_results:
            attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            match_classification = attrs.get("match_classification") or attrs.get("match_type") or attrs.get("classification")
            
            if match_classification in ("SKILL_PARTIAL_MATCH", "partial"):
                skill_name = attrs.get("job_skill_name") or attrs.get("resume_skill_name") or result.job_feature_id
                if skill_name not in partial_skills:
                    partial_skills.append(skill_name)

        for skill in partial_skills:
            if self._rules.should_recommend("SKILL_PARTIAL_MATCH"):
                rec = SkillRecommendationBuilder.build_partial_recommendation(skill, index)
                recommendations.append(rec)
                index += 1

        # Workload telemetry calculations
        skills_processed = len(missing_skills) + len(skill_results)

        # 3. Validate generated recommendations
        SkillRecommendationValidator.validate(recommendations)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # 4. Compile statistics
        self._last_statistics = SkillRecommendationStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            missing_skills=len(missing_skills),
            partial_skills=len(partial_skills),
            recommendations_generated=len(recommendations),
            skills_processed=skills_processed,
            success=True,
        )

        return tuple(recommendations)
