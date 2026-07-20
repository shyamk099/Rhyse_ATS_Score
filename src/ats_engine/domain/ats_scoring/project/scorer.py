"""ProjectScorer implementation.

Purpose:
    Expose abstract interfaces compliance for calculating project scores.
"""

from __future__ import annotations

import time
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import BaseSectionScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules
from ats_engine.domain.ats_scoring.project.validator import ProjectScoreValidator
from ats_engine.domain.ats_scoring.project.resolver import ProjectClassification, ProjectClassificationResolver
from ats_engine.domain.ats_scoring.project.breakdown_builder import ProjectBreakdownBuilder
from ats_engine.domain.ats_scoring.project.statistics_builder import ProjectStatisticsBuilder


class ProjectScorer(BaseSectionScorer):
    """Concrete scorer implementation executing deterministic project weight calculations."""

    def __init__(self) -> None:
        """Initialize telemetry and metadata maps."""
        super().__init__()
        self._metadata.update({
            "engine_version": "1.0.0",
            "rules_version": "1.0.0",
            "pipeline_version": "1.0.0",
        })
        self._resolver = ProjectClassificationResolver()

    def _resolve_rules(self, context: ScoringContext) -> ProjectScoringRules:
        """Resolve ProjectScoringRules from the context. Fallback to default if not configured."""
        if isinstance(context.rules, ProjectScoringRules):
            return context.rules
        return ProjectScoringRules()

    def validate(self, context: ScoringContext) -> None:
        """Execute read-only structural validation on match results.

        Raises:
            ProjectValidationError: If duplicate matching pairs or null blocks exist.
        """
        proj_rules = self._resolve_rules(context)
        proj_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ProjectMatcher"
        ]
        ProjectScoreValidator.validate(proj_results, proj_rules)

    def score(self, context: ScoringContext) -> SectionScore:
        """Perform deterministic calculations and return SectionScore."""
        return self.build(context)

    def build(self, context: ScoringContext) -> SectionScore:
        """Validate context, calculate scores, build breakdown, compile stats and return SectionScore."""
        start_time = time.perf_counter()
        
        # Validate first
        self.validate(context)

        proj_rules = self._resolve_rules(context)
        proj_results = [
            r for r in context.match_collection.results
            if getattr(r, "matcher_type", None) == "ProjectMatcher"
        ]

        exact_matches = 0
        similar_projects = 0
        related_projects = 0
        partial_matches = 0

        for r in proj_results:
            classification = self._resolver.resolve(r)
            if classification == ProjectClassification.EXACT_MATCH:
                exact_matches += 1
            elif classification == ProjectClassification.SIMILAR_PROJECT:
                similar_projects += 1
            elif classification == ProjectClassification.RELATED_PROJECT:
                related_projects += 1
            elif classification == ProjectClassification.PARTIAL_MATCH:
                partial_matches += 1

        raw_points = (
            (exact_matches * proj_rules.exact_match_weight) +
            (similar_projects * proj_rules.similar_project_weight) +
            (related_projects * proj_rules.related_project_weight) +
            (partial_matches * proj_rules.partial_match_weight)
        )

        # Clamping raw points between minimum and maximum scores
        raw_score = min(raw_points, proj_rules.maximum_project_score)
        raw_score = max(raw_score, proj_rules.minimum_project_score)

        # Count matched and missing items
        matched_count = len(proj_results)
        
        # Pull missing project count from first result if side-channel configured
        missing_count = 0
        if proj_results:
            first_attrs = getattr(proj_results[0].metadata, "custom_attributes", {}) or {}
            missing_proj = first_attrs.get("missing_projects", [])
            if isinstance(missing_proj, (list, tuple)):
                missing_count = len(missing_proj)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Update telemetry statistics dict
        self._stats = ProjectStatisticsBuilder.build(
            matched_items=matched_count,
            missing_items=missing_count,
            exact_matches=exact_matches,
            similar_projects=similar_projects,
            related_projects=related_projects,
            partial_matches=partial_matches,
            processing_time_ms=processing_time_ms,
        )

        # Build ScoreBreakdown
        breakdown = ProjectBreakdownBuilder.build(
            results=proj_results,
            exact_matches=exact_matches,
            similar_projects=similar_projects,
            related_projects=related_projects,
            partial_matches=partial_matches,
            raw_points=raw_score,
            maximum_points=proj_rules.maximum_project_score,
            rules_version=proj_rules.version,
        )

        return SectionScore(
            section_name="PROJECT",
            raw_score=raw_score,
            normalized_score=None,
            maximum_score=proj_rules.maximum_project_score,
            weight=None,
            breakdown=breakdown,
            metadata={},
        )

