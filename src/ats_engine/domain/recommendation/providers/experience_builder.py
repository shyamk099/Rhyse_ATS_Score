"""ExperienceRecommendationBuilder definition.

Purpose:
    Isolate construction logic for experience recommendations.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.recommendation.models import Recommendation


class ExperienceRecommendationBuilder:
    """Builder producing deterministic Recommendation DTOs for Experience features."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Helper to normalize names into deterministic ID components."""
        return name.upper().strip().replace(" ", "_").replace("-", "_")

    @classmethod
    def build_missing_recommendation(
        cls,
        experience_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a missing experience requirement.

        Args:
            experience_name: The name of the missing experience requirement.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(experience_name)
        rec_id = f"EXP_MISSING_{norm_name}"
        title = f"{experience_name} experience is missing"
        description = f"The job description requires {experience_name} experience but it was not found in the resume."

        return Recommendation(
            recommendation_id=rec_id,
            section="experience",
            category="EXPERIENCE_MISSING",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_partial_recommendation(
        cls,
        experience_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for partially matched experience.

        Args:
            experience_name: The name of the partially matched experience.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(experience_name)
        rec_id = f"EXP_PARTIAL_{norm_name}"
        title = f"Expand {experience_name} experience"
        description = f"The resume contains partially matching {experience_name} experience."

        return Recommendation(
            recommendation_id=rec_id,
            section="experience",
            category="EXPERIENCE_PARTIAL_MATCH",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_duration_gap_recommendation(
        cls,
        experience_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for insufficient duration gap.

        Args:
            experience_name: The name of the experience requirement.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(experience_name)
        rec_id = f"EXP_DURATION_{norm_name}"
        title = f"Increase {experience_name} duration"
        description = f"The resume has insufficient duration for required {experience_name} experience."

        return Recommendation(
            recommendation_id=rec_id,
            section="experience",
            category="EXPERIENCE_DURATION_GAP",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )
