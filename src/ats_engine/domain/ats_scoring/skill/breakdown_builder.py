"""SkillBreakdownBuilder definition.

Purpose:
    Provide construction builder for Skill domain ScoreBreakdowns using generic fields.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class SkillBreakdownBuilder:
    """Builder assembling detailed matching lists and counts into generic ScoreBreakdown DTOs."""

    @staticmethod
    def build(
        results: Sequence[MatchResult],
        mandatory_matches: int,
        optional_matches: int,
        raw_points: float,
        maximum_points: float,
        rules_version: str,
    ) -> ScoreBreakdown:
        """Construct the immutable ScoreBreakdown DTO using generic fields."""
        matched_items = []
        missing_items = []

        for result in results:
            custom_attrs = getattr(result.metadata, "custom_attributes", {}) or {}
            skill_name = custom_attrs.get("job_skill_name") or custom_attrs.get("resume_skill_name") or result.job_feature_id
            matched_items.append(skill_name)

            if "missing_skills" in custom_attrs:
                missing = custom_attrs["missing_skills"]
                if isinstance(missing, (list, tuple)):
                    for m in missing:
                        if m not in missing_items:
                            missing_items.append(m)

        classification_counts = {
            "mandatory": mandatory_matches,
            "optional": optional_matches,
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
