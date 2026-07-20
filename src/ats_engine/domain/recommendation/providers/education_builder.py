"""EducationRecommendationBuilder definition.

Purpose:
    Isolate construction logic for education recommendations.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.recommendation.models import Recommendation


class EducationRecommendationBuilder:
    """Builder producing deterministic Recommendation DTOs for Education features."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Helper to normalize names into deterministic ID components."""
        return name.upper().strip().replace(" ", "_").replace("-", "_")

    @classmethod
    def build_missing_recommendation(
        cls,
        education_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a missing education requirement.

        Args:
            education_name: The name of the missing education requirement (e.g. 'Bachelor').
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(education_name)
        rec_id = f"EDU_MISSING_{norm_name}"
        title = f"{education_name} degree is missing"
        description = f"The job description requires a {education_name} degree but it was not found in the resume."

        return Recommendation(
            recommendation_id=rec_id,
            section="education",
            category="EDUCATION_MISSING",
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
        education_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for partially matched education.

        Args:
            education_name: The name of the partially matched education.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(education_name)
        rec_id = f"EDU_PARTIAL_{norm_name}"
        title = f"Expand {education_name} education details"
        description = f"The resume contains partially matching or field-unrelated {education_name} education."

        return Recommendation(
            recommendation_id=rec_id,
            section="education",
            category="EDUCATION_PARTIAL_MATCH",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_level_gap_recommendation(
        cls,
        education_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a qualification level gap.

        Args:
            education_name: The name of the required education level.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(education_name)
        rec_id = f"EDU_LEVEL_GAP_{norm_name}"
        title = f"Upgrade to {education_name} qualification"
        description = f"The resume has a lower qualification level than the required {education_name} degree."

        return Recommendation(
            recommendation_id=rec_id,
            section="education",
            category="EDUCATION_LEVEL_GAP",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )
