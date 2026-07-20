"""CertificationScorer implementation.

Purpose:
    Expose abstract interfaces compliance for calculating certification scores.
"""

from __future__ import annotations

import time
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import BaseSectionScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules
from ats_engine.domain.ats_scoring.certification.validator import CertificationScoreValidator
from ats_engine.domain.ats_scoring.certification.resolver import CertificationClassification, CertificationClassificationResolver
from ats_engine.domain.ats_scoring.certification.breakdown_builder import CertificationBreakdownBuilder
from ats_engine.domain.ats_scoring.certification.statistics_builder import CertificationStatisticsBuilder


class CertificationScorer(BaseSectionScorer):
    """Concrete scorer implementation executing deterministic certification weight calculations."""

    def __init__(self) -> None:
        """Initialize telemetry and metadata maps."""
        super().__init__()
        self._metadata.update({
            "engine_version": "1.0.0",
            "rules_version": "1.0.0",
            "pipeline_version": "1.0.0",
        })
        self._resolver = CertificationClassificationResolver()

    def _resolve_rules(self, context: ScoringContext) -> CertificationScoringRules:
        """Resolve CertificationScoringRules from the context. Fallback to default if not configured."""
        if isinstance(context.rules, CertificationScoringRules):
            return context.rules
        return CertificationScoringRules()

    def validate(self, context: ScoringContext) -> None:
        """Execute read-only structural validation on match results.

        Raises:
            CertificationValidationError: If duplicate matching pairs or null blocks exist.
        """
        cert_rules = self._resolve_rules(context)
        cert_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "CertificationMatcher"
        ]
        CertificationScoreValidator.validate(cert_results, cert_rules)

    def score(self, context: ScoringContext) -> SectionScore:
        """Perform deterministic calculations and return SectionScore."""
        return self.build(context)

    def build(self, context: ScoringContext) -> SectionScore:
        """Validate context, calculate scores, build breakdown, compile stats and return SectionScore."""
        start_time = time.perf_counter()
        
        # Validate first
        self.validate(context)

        cert_rules = self._resolve_rules(context)
        cert_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "CertificationMatcher"
        ]

        exact_matches = 0
        equivalent_certifications = 0
        related_certifications = 0
        partial_matches = 0
        expired_certifications = 0

        for r in cert_results:
            classification = self._resolver.resolve(r)
            if classification == CertificationClassification.EXACT_MATCH:
                exact_matches += 1
            elif classification == CertificationClassification.EQUIVALENT_CERTIFICATION:
                equivalent_certifications += 1
            elif classification == CertificationClassification.RELATED_CERTIFICATION:
                related_certifications += 1
            elif classification == CertificationClassification.PARTIAL_MATCH:
                partial_matches += 1
            elif classification == CertificationClassification.EXPIRED_CERTIFICATION:
                expired_certifications += 1

        expired_weight = cert_rules.expired_certification_weight if cert_rules.count_expired_certifications else 0.0

        raw_points = (
            (exact_matches * cert_rules.exact_match_weight) +
            (equivalent_certifications * cert_rules.equivalent_certification_weight) +
            (related_certifications * cert_rules.related_certification_weight) +
            (partial_matches * cert_rules.partial_match_weight) +
            (expired_certifications * expired_weight)
        )

        # Clamping raw points between minimum and maximum scores
        raw_score = min(raw_points, cert_rules.maximum_certification_score)
        raw_score = max(raw_score, cert_rules.minimum_certification_score)

        # Count matched and missing items
        matched_count = len(cert_results)
        
        # Pull missing certification count from first result if side-channel configured
        missing_count = 0
        if cert_results:
            first_attrs = getattr(cert_results[0].metadata, "custom_attributes", {}) or {}
            missing_cert = first_attrs.get("missing_certifications", [])
            if isinstance(missing_cert, (list, tuple)):
                missing_count = len(missing_cert)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Update telemetry statistics dict
        self._stats = CertificationStatisticsBuilder.build(
            matched_items=matched_count,
            missing_items=missing_count,
            exact_matches=exact_matches,
            equivalent_certifications=equivalent_certifications,
            related_certifications=related_certifications,
            partial_matches=partial_matches,
            expired_certifications=expired_certifications,
            processing_time_ms=processing_time_ms,
        )

        # Build ScoreBreakdown
        breakdown = CertificationBreakdownBuilder.build(
            results=cert_results,
            exact_matches=exact_matches,
            equivalent_certifications=equivalent_certifications,
            related_certifications=related_certifications,
            partial_matches=partial_matches,
            expired_certifications=expired_certifications,
            raw_points=raw_score,
            maximum_points=cert_rules.maximum_certification_score,
            rules_version=cert_rules.version,
        )

        return SectionScore(
            section_name="CERTIFICATION",
            raw_score=raw_score,
            normalized_score=None,
            maximum_score=cert_rules.maximum_certification_score,
            weight=None,
            breakdown=breakdown,
            metadata={},
        )

