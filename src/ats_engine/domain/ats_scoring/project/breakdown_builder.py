"""ProjectBreakdownBuilder definition.

Purpose:
    Provide construction builder for Project domain ScoreBreakdowns.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class ProjectBreakdownBuilder:
    """Builder assembling detailed matching lists and counts into generic ScoreBreakdown DTOs."""

    @staticmethod
    def build(
        results: Sequence[MatchResult],
        exact_matches: int,
        similar_projects: int,
        related_projects: int,
        partial_matches: int,
        raw_points: float,
        maximum_points: float,
        rules_version: str,
    ) -> ScoreBreakdown:
        """Construct the immutable ScoreBreakdown DTO using generic fields."""
        matched_items = []
        missing_items = []

        for result in results:
            custom_attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            proj_name = custom_attrs.get("job_project_name") or custom_attrs.get("resume_project_name") or result.job_feature_id
            matched_items.append(proj_name)

            if "missing_projects" in custom_attrs:
                missing = custom_attrs["missing_projects"]
                if isinstance(missing, (list, tuple)):
                    for m in missing:
                        if m not in missing_items:
                            missing_items.append(m)

        classification_counts = {
            "exact_match": exact_matches,
            "similar_project": similar_projects,
            "related_project": related_projects,
            "partial_match": partial_matches,
        }

        return ScoreBreakdown(
            matched_items=tuple(matched_items),
            missing_items=tuple(missing_items),
            classification_counts=classification_counts,
            raw_points=raw_points,
            maximum_points=maximum_points,
            rules_version=rules_version,
            metadata={},
        )

