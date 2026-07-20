"""EducationBreakdownBuilder definition.

Purpose:
    Provide construction builder for Education domain ScoreBreakdowns.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class EducationBreakdownBuilder:
    """Builder assembling detailed matching lists and counts into generic ScoreBreakdown DTOs."""

    @staticmethod
    def build(
        results: Sequence[MatchResult],
        exact_matches: int,
        higher_than_required: int,
        related_field: int,
        lower_than_required: int,
        unrelated_field: int,
        raw_points: float,
        maximum_points: float,
        rules_version: str,
    ) -> ScoreBreakdown:
        """Construct the immutable ScoreBreakdown DTO using generic fields."""
        matched_items = []
        missing_items = []

        for result in results:
            custom_attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            edu_name = custom_attrs.get("job_education_name") or custom_attrs.get("resume_education_name") or result.job_feature_id
            matched_items.append(edu_name)

            if "missing_education" in custom_attrs:
                missing = custom_attrs["missing_education"]
                if isinstance(missing, (list, tuple)):
                    for m in missing:
                        if m not in missing_items:
                            missing_items.append(m)

        classification_counts = {
            "exact_match": exact_matches,
            "higher_than_required": higher_than_required,
            "related_field": related_field,
            "lower_than_required": lower_than_required,
            "unrelated_field": unrelated_field,
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

