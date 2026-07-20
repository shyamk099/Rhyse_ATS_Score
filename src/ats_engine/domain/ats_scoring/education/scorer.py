"""EducationScorer implementation.

Purpose:
    Expose abstract interfaces compliance for calculating education scores.
"""

from __future__ import annotations

import time
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import BaseSectionScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules
from ats_engine.domain.ats_scoring.education.validator import EducationScoreValidator
from ats_engine.domain.ats_scoring.education.resolver import EducationClassification, EducationClassificationResolver
from ats_engine.domain.ats_scoring.education.breakdown_builder import EducationBreakdownBuilder
from ats_engine.domain.ats_scoring.education.statistics_builder import EducationStatisticsBuilder


class EducationScorer(BaseSectionScorer):
    """Concrete scorer implementation executing deterministic education weight calculations."""

    def __init__(self) -> None:
        """Initialize telemetry and metadata maps."""
        super().__init__()
        self._metadata.update({
            "engine_version": "1.0.0",
            "rules_version": "1.0.0",
            "pipeline_version": "1.0.0",
        })
        self._resolver = EducationClassificationResolver()

    def _resolve_rules(self, context: ScoringContext) -> EducationScoringRules:
        """Resolve EducationScoringRules from the context. Fallback to default if not configured."""
        if isinstance(context.rules, EducationScoringRules):
            return context.rules
        return EducationScoringRules()

    def validate(self, context: ScoringContext) -> None:
        """Execute read-only structural validation on match results.

        Raises:
            EducationValidationError: If duplicate matching pairs or null blocks exist.
        """
        edu_rules = self._resolve_rules(context)
        edu_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "EducationMatcher"
        ]
        EducationScoreValidator.validate(edu_results, edu_rules)

    def score(self, context: ScoringContext) -> SectionScore:
        """Perform deterministic calculations and return SectionScore."""
        return self.build(context)

    def build(self, context: ScoringContext) -> SectionScore:
        """Validate context, calculate scores, build breakdown, compile stats and return SectionScore."""
        start_time = time.perf_counter()
        
        # Validate first
        self.validate(context)

        edu_rules = self._resolve_rules(context)
        edu_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "EducationMatcher"
        ]

        exact_matches = 0
        higher_than_required = 0
        related_field = 0
        lower_than_required = 0
        unrelated_field = 0

        for r in edu_results:
            classification = self._resolver.resolve(r)
            if classification == EducationClassification.EXACT_MATCH:
                exact_matches += 1
            elif classification == EducationClassification.HIGHER_THAN_REQUIRED:
                higher_than_required += 1
            elif classification == EducationClassification.RELATED_FIELD:
                related_field += 1
            elif classification == EducationClassification.LOWER_THAN_REQUIRED:
                lower_than_required += 1
            elif classification == EducationClassification.UNRELATED_FIELD:
                unrelated_field += 1

        raw_points = (
            (exact_matches * edu_rules.exact_match_weight) +
            (higher_than_required * edu_rules.higher_than_required_weight) +
            (related_field * edu_rules.related_field_weight) +
            (lower_than_required * edu_rules.lower_than_required_weight) +
            (unrelated_field * edu_rules.unrelated_field_weight)
        )

        # Clamping raw points between minimum and maximum scores
        raw_score = min(raw_points, edu_rules.maximum_education_score)
        raw_score = max(raw_score, edu_rules.minimum_education_score)

        # Count matched and missing items
        matched_count = len(edu_results)
        
        # Pull missing education count from first result if side-channel configured
        missing_count = 0
        if edu_results:
            first_attrs = getattr(edu_results[0].metadata, "custom_attributes", {}) or {}
            missing_edu = first_attrs.get("missing_education", [])
            if isinstance(missing_edu, (list, tuple)):
                missing_count = len(missing_edu)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Update telemetry statistics dict
        self._stats = EducationStatisticsBuilder.build(
            matched_items=matched_count,
            missing_items=missing_count,
            exact_matches=exact_matches,
            higher_than_required=higher_than_required,
            related_field=related_field,
            lower_than_required=lower_than_required,
            unrelated_field=unrelated_field,
            processing_time_ms=processing_time_ms,
        )

        # Build ScoreBreakdown
        breakdown = EducationBreakdownBuilder.build(
            results=edu_results,
            exact_matches=exact_matches,
            higher_than_required=higher_than_required,
            related_field=related_field,
            lower_than_required=lower_than_required,
            unrelated_field=unrelated_field,
            raw_points=raw_score,
            maximum_points=edu_rules.maximum_education_score,
            rules_version=edu_rules.version,
        )

        return SectionScore(
            section_name="EDUCATION",
            raw_score=raw_score,
            normalized_score=None,
            maximum_score=edu_rules.maximum_education_score,
            weight=None,
            breakdown=breakdown,
            metadata={},
        )

