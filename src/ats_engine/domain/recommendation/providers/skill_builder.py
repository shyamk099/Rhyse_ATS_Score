"""SkillRecommendationBuilder definition.

Purpose:
    Isolate construction logic for skill recommendations.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.recommendation.models import Recommendation


class SkillRecommendationBuilder:
    """Builder constructing deterministic Recommendation DTOs for Skill features."""

    @staticmethod
    def build_missing_recommendation(
        skill_name: str,
        index: int,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a missing skill.

        Args:
            skill_name: The name of the missing skill.
            index: Positional index for generating unique ID.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        rec_id = f"REC-SKILL-MISSING-{index}"
        title = f"{skill_name} is missing"
        description = f"The job description requires {skill_name} but it was not found in the resume."

        return Recommendation(
            recommendation_id=rec_id,
            section="skill",
            category="SKILL_MISSING",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @staticmethod
    def build_partial_recommendation(
        skill_name: str,
        index: int,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a partially matched skill.

        Args:
            skill_name: The name of the partially matched skill.
            index: Positional index for generating unique ID.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        rec_id = f"REC-SKILL-PARTIAL-{index}"
        title = f"Expand {skill_name} experience"
        description = f"The resume contains a partially matching {skill_name} skill."

        return Recommendation(
            recommendation_id=rec_id,
            section="skill",
            category="SKILL_PARTIAL_MATCH",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )
