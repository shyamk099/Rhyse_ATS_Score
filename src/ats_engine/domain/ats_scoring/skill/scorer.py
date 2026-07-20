"""SkillScorer implementation.

Purpose:
    Expose abstract interfaces compliance for calculating skill scores.
"""

from __future__ import annotations

import time
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import BaseSectionScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules
from ats_engine.domain.ats_scoring.skill.validator import SkillScoreValidator
from ats_engine.domain.ats_scoring.skill.resolver import SkillClassification, SkillClassificationResolver
from ats_engine.domain.ats_scoring.skill.breakdown_builder import SkillBreakdownBuilder
from ats_engine.domain.ats_scoring.skill.statistics_builder import SkillStatisticsBuilder


class SkillScorer(BaseSectionScorer):
    """Concrete scorer implementation executing deterministic skill weight calculations."""

    def __init__(self) -> None:
        """Initialize telemetry and metadata maps."""
        super().__init__()
        self._metadata.update({
            "engine_version": "1.0.0",
            "rules_version": "1.0.0",
            "pipeline_version": "1.0.0",
        })
        self._resolver = SkillClassificationResolver()

    def _resolve_rules(self, context: ScoringContext) -> SkillScoringRules:
        """Resolve SkillScoringRules from the context. Fallback to default if not configured."""
        if isinstance(context.rules, SkillScoringRules):
            return context.rules
        return SkillScoringRules()

    def validate(self, context: ScoringContext) -> None:
        """Execute read-only structural validation on match results.

        Raises:
            SkillValidationError: If duplicate matching pairs or null blocks exist.
        """
        skill_rules = self._resolve_rules(context)
        skill_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "SkillMatcher"
        ]
        SkillScoreValidator.validate(skill_results, skill_rules)

    def score(self, context: ScoringContext) -> SectionScore:
        """Perform deterministic calculations and return SectionScore."""
        return self.build(context)

    def build(self, context: ScoringContext) -> SectionScore:
        """Validate context, calculate scores, build breakdown, compile stats and return SectionScore."""
        start_time = time.perf_counter()
        
        # Validate first
        self.validate(context)

        skill_rules = self._resolve_rules(context)
        skill_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "SkillMatcher"
        ]

        mandatory_matches = 0
        optional_matches = 0

        for r in skill_results:
            classification = self._resolver.resolve(r)
            if classification == SkillClassification.MANDATORY:
                mandatory_matches += 1
            else:
                optional_matches += 1

        raw_points = (
            (mandatory_matches * skill_rules.mandatory_skill_weight) +
            (optional_matches * skill_rules.optional_skill_weight)
        )

        # Clamping raw points between minimum and maximum scores
        raw_score = min(raw_points, skill_rules.maximum_skill_score)
        raw_score = max(raw_score, skill_rules.minimum_skill_score)

        # Count matched and missing items
        matched_count = len(skill_results)
        
        # Pull missing skills count from first result if side-channel configured
        missing_count = 0
        if skill_results:
            first_attrs = getattr(skill_results[0].metadata, "custom_attributes", {}) or {}
            missing_skills = first_attrs.get("missing_skills", [])
            if isinstance(missing_skills, (list, tuple)):
                missing_count = len(missing_skills)

        total_skills = matched_count + missing_count

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Update telemetry statistics dict
        self._stats = SkillStatisticsBuilder.build(
            matched_items=matched_count,
            missing_items=missing_count,
            mandatory_matches=mandatory_matches,
            optional_matches=optional_matches,
            raw_points=raw_score,
            total_items=total_skills,
            processing_time_ms=processing_time_ms,
        )

        # Build ScoreBreakdown
        breakdown = SkillBreakdownBuilder.build(
            results=skill_results,
            mandatory_matches=mandatory_matches,
            optional_matches=optional_matches,
            raw_points=raw_score,
            maximum_points=skill_rules.maximum_skill_score,
            rules_version=skill_rules.version,
        )

        return SectionScore(
            section_name="SKILL",
            raw_score=raw_score,
            normalized_score=None,
            maximum_score=skill_rules.maximum_skill_score,
            weight=None,
            breakdown=breakdown,
            metadata={},
        )
