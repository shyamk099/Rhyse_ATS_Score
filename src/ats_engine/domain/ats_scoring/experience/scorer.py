"""ExperienceScorer implementation.

Purpose:
    Expose abstract interfaces compliance for calculating experience scores.
"""

from __future__ import annotations

import time
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import BaseSectionScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules
from ats_engine.domain.ats_scoring.experience.validator import ExperienceScoreValidator
from ats_engine.domain.ats_scoring.experience.resolver import ExperienceClassification, ExperienceClassificationResolver
from ats_engine.domain.ats_scoring.experience.breakdown_builder import ExperienceBreakdownBuilder
from ats_engine.domain.ats_scoring.experience.statistics_builder import ExperienceStatisticsBuilder


class ExperienceScorer(BaseSectionScorer):
    """Concrete scorer implementation executing deterministic experience weight calculations."""

    def __init__(self) -> None:
        """Initialize telemetry and metadata maps."""
        super().__init__()
        self._metadata.update({
            "engine_version": "1.0.0",
            "rules_version": "1.0.0",
            "pipeline_version": "1.0.0",
        })
        self._resolver = ExperienceClassificationResolver()

    def _resolve_rules(self, context: ScoringContext) -> ExperienceScoringRules:
        """Resolve ExperienceScoringRules from the context. Fallback to default if not configured."""
        if isinstance(context.rules, ExperienceScoringRules):
            return context.rules
        return ExperienceScoringRules()

    def validate(self, context: ScoringContext) -> None:
        """Execute read-only structural validation on match results.

        Raises:
            ExperienceValidationError: If duplicate matching pairs or null blocks exist.
        """
        exp_rules = self._resolve_rules(context)
        exp_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ExperienceMatcher"
        ]
        ExperienceScoreValidator.validate(exp_results, exp_rules)

    def score(self, context: ScoringContext) -> SectionScore:
        """Perform deterministic calculations and return SectionScore."""
        return self.build(context)

    def build(self, context: ScoringContext) -> SectionScore:
        """Validate context, calculate scores, build breakdown, compile stats and return SectionScore."""
        start_time = time.perf_counter()
        
        # Validate first
        self.validate(context)

        exp_rules = self._resolve_rules(context)
        exp_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ExperienceMatcher"
        ]

        exact_matches = 0
        partial_matches = 0
        overqualified_matches = 0
        underqualified_matches = 0

        for r in exp_results:
            classification = self._resolver.resolve(r)
            if classification == ExperienceClassification.EXACT_MATCH:
                exact_matches += 1
            elif classification == ExperienceClassification.PARTIAL_MATCH:
                partial_matches += 1
            elif classification == ExperienceClassification.OVERQUALIFIED:
                overqualified_matches += 1
            elif classification == ExperienceClassification.UNDERQUALIFIED:
                underqualified_matches += 1

        raw_points = (
            (exact_matches * exp_rules.exact_match_weight) +
            (partial_matches * exp_rules.partial_match_weight) +
            (overqualified_matches * exp_rules.overqualified_weight) +
            (underqualified_matches * exp_rules.underqualified_weight)
        )

        # Clamping raw points between minimum and maximum scores
        raw_score = min(raw_points, exp_rules.maximum_experience_score)
        raw_score = max(raw_score, exp_rules.minimum_experience_score)

        # Count matched and missing items
        matched_count = len(exp_results)
        
        # Pull missing experience count from first result if side-channel configured
        missing_count = 0
        if exp_results:
            first_attrs = getattr(exp_results[0].metadata, "custom_attributes", {}) or {}
            missing_exp = first_attrs.get("missing_experience", [])
            if isinstance(missing_exp, (list, tuple)):
                missing_count = len(missing_exp)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Update telemetry statistics dict
        self._stats = ExperienceStatisticsBuilder.build(
            matched_items=matched_count,
            missing_items=missing_count,
            exact_matches=exact_matches,
            partial_matches=partial_matches,
            overqualified_matches=overqualified_matches,
            underqualified_matches=underqualified_matches,
            processing_time_ms=processing_time_ms,
        )

        # Build ScoreBreakdown
        breakdown = ExperienceBreakdownBuilder.build(
            results=exp_results,
            exact_matches=exact_matches,
            partial_matches=partial_matches,
            overqualified_matches=overqualified_matches,
            underqualified_matches=underqualified_matches,
            raw_points=raw_score,
            maximum_points=exp_rules.maximum_experience_score,
            rules_version=exp_rules.version,
        )

        return SectionScore(
            section_name="EXPERIENCE",
            raw_score=raw_score,
            normalized_score=None,
            maximum_score=exp_rules.maximum_experience_score,
            weight=None,
            breakdown=breakdown,
            metadata={},
        )
