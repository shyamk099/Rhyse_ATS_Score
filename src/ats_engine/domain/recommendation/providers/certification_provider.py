"""CertificationRecommendationProvider implementation.

Purpose:
    Expose concrete BaseRecommendationProvider implementing deterministic certification recommendations.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider, RecommendationAction
from ats_engine.domain.recommendation.providers.certification_rules import CertificationRecommendationRules
from ats_engine.domain.recommendation.providers.certification_builder import CertificationRecommendationBuilder
from ats_engine.domain.recommendation.providers.certification_validator import CertificationRecommendationValidator
from ats_engine.domain.recommendation.providers.certification_statistics_builder import CertificationRecommendationStatisticsBuilder

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class CertificationRecommendationProvider(BaseRecommendationProvider):
    """Provider analyzing MatchCollection and ScoreResult to suggest certification improvements."""

    PROVIDER_NAME: str = "CERTIFICATION"
    PRIORITY: int = 500

    def __init__(self, rules: CertificationRecommendationRules | None = None) -> None:
        """Initialize the provider with optional rules."""
        self._rules = rules or CertificationRecommendationRules()
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
        """Validate inputs required for certification recommendations.

        Requires:
            - context.score_result.certification_score is not None.
        """
        if getattr(context.score_result, "certification_score", None) is None:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(
                "CertificationRecommendationProvider failed validation: "
                "missing certification_score in ScoreResult."
            )

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        """Produce deterministic Certification Recommendation DTOs.

        Lifecycle:
            1. Extract missing certifications from score_result breakdown.
            2. Extract partial matches and expired certifications from match_collection.
            3. Apply rules to filter recommendations.
            4. Construct DTOs using builder.
            5. Validate output list.
            6. Return final tuple.
        """
        start_time = time.perf_counter()
        self.validate(context)

        recommendations: list[Recommendation] = []

        # 1. Missing Certifications (from ScoreResult breakdown)
        missing_count = 0
        cert_score = context.score_result.certification_score
        missing_list: tuple[str, ...] = ()
        if cert_score and cert_score.breakdown:
            missing_list = cert_score.breakdown.missing_items

        for item in missing_list:
            action = self._rules.evaluate_missing(item)
            if action == RecommendationAction.MISSING:
                rec = CertificationRecommendationBuilder.build_missing_recommendation(item)
                recommendations.append(rec)
                missing_count += 1

        # 2. Matched Certifications (from MatchResults)
        partial_count = 0
        expired_count = 0
        exact_matches = 0
        equivalent_matches = 0

        cert_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "CertificationMatcher"
        ]

        for result in cert_results:
            attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            cert_name = attrs.get("job_certification_name") or attrs.get("resume_certification_name") or result.job_feature_id

            action = self._rules.evaluate_match(result)
            if action == RecommendationAction.PARTIAL:
                rec = CertificationRecommendationBuilder.build_partial_recommendation(cert_name)
                recommendations.append(rec)
                partial_count += 1
            elif action == RecommendationAction.EXPIRED:
                rec = CertificationRecommendationBuilder.build_expired_recommendation(cert_name)
                recommendations.append(rec)
                expired_count += 1
            else:
                val = (attrs.get("match_type") or attrs.get("classification") or "").upper()
                if val in ("EXACT_MATCH", "EXACT"):
                    exact_matches += 1
                else:
                    equivalent_matches += 1

        # Workload telemetry calculations
        certifications_processed = len(missing_list) + len(cert_results)

        # 3. Validate generated recommendations
        CertificationRecommendationValidator.validate(recommendations)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # 4. Compile statistics
        self._last_statistics = CertificationRecommendationStatisticsBuilder.build(
            execution_time_ms=duration_ms,
            certifications_processed=certifications_processed,
            missing_certifications=missing_count,
            partial_matches=partial_count,
            expired_certifications=expired_count,
            exact_matches=exact_matches,
            equivalent_matches=equivalent_matches,
            recommendations_generated=len(recommendations),
            success=True,
        )

        return tuple(recommendations)
