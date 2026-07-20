"""ProjectRecommendationBuilder definition.

Purpose:
    Isolate construction logic for project recommendations.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.recommendation.models import Recommendation


class ProjectRecommendationBuilder:
    """Builder producing deterministic Recommendation DTOs for Project features."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Helper to normalize names into deterministic ID components."""
        return name.upper().strip().replace(" ", "_").replace("-", "_")

    @classmethod
    def build_missing_recommendation(
        cls,
        project_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a missing project requirement.

        Args:
            project_name: The name of the missing project requirement.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(project_name)
        rec_id = f"PROJ_MISSING_{norm_name}"
        title = f"{project_name} project is missing"
        description = f"The job description requires a {project_name} project but no matching project was found in the resume."

        return Recommendation(
            recommendation_id=rec_id,
            section="project",
            category="PROJECT_MISSING",
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
        project_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for partially matched project.

        Args:
            project_name: The name of the partially matched project.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(project_name)
        rec_id = f"PROJ_PARTIAL_{norm_name}"
        title = f"Expand {project_name} project details"
        description = f"The resume contains a partially matching project for {project_name}."

        return Recommendation(
            recommendation_id=rec_id,
            section="project",
            category="PROJECT_PARTIAL_MATCH",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_related_gap_recommendation(
        cls,
        project_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a related project gap.

        Args:
            project_name: The name of the required project type.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(project_name)
        rec_id = f"PROJ_RELATED_{norm_name}"
        title = f"Add related {project_name} project"
        description = f"The resume has similar but not exact project alignment with required {project_name}."

        return Recommendation(
            recommendation_id=rec_id,
            section="project",
            category="PROJECT_RELATED_GAP",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )
