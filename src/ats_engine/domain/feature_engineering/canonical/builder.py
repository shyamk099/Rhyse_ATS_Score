"""Builder producing immutable CanonicalFeatureCollection payloads.

Purpose:
    Deteriministically sort category features and compile the unified collection DTO
    without business scoring or ranking logic.
"""

from __future__ import annotations

from typing import Any, Mapping

from ats_engine.domain.feature_engineering.models import (
    CanonicalFeatureCollection,
    FeatureCollection,
    FeatureStatistics,
    ValidationSummary,
)


class CanonicalFeatureCollectionBuilder:
    """Builder constructing consolidated CanonicalFeatureCollection DTOs."""

    @classmethod
    def build(
        cls,
        skills: FeatureCollection,
        experience: FeatureCollection,
        education: FeatureCollection,
        projects: FeatureCollection,
        certifications: FeatureCollection,
        statistics: FeatureStatistics,
        validation_summary: ValidationSummary,
        metadata: Mapping[str, Any] | None = None,
    ) -> CanonicalFeatureCollection:
        """Assemble all features deterministically into CanonicalFeatureCollection (Refinement 5).

        Args:
            skills: Skill FeatureCollection.
            experience: Experience FeatureCollection.
            education: Education FeatureCollection.
            projects: Project FeatureCollection.
            certifications: Certification FeatureCollection.
            statistics: Compiled FeatureStatistics.
            validation_summary: Audit ValidationSummary DTO.
            metadata: Custom attributes tracker.

        Returns:
            The consolidated CanonicalFeatureCollection.
        """
        # Ensure deterministic ordering within each category (Refinement 5)
        sorted_skills = FeatureCollection(
            features=tuple(sorted(skills.features, key=lambda f: f.feature_id)),
            statistics=skills.statistics,
            context=skills.context,
        )
        sorted_experience = FeatureCollection(
            features=tuple(sorted(experience.features, key=lambda f: f.feature_id)),
            statistics=experience.statistics,
            context=experience.context,
        )
        sorted_education = FeatureCollection(
            features=tuple(sorted(education.features, key=lambda f: f.feature_id)),
            statistics=education.statistics,
            context=education.context,
        )
        sorted_projects = FeatureCollection(
            features=tuple(sorted(projects.features, key=lambda f: f.feature_id)),
            statistics=projects.statistics,
            context=projects.context,
        )
        sorted_certifications = FeatureCollection(
            features=tuple(sorted(certifications.features, key=lambda f: f.feature_id)),
            statistics=certifications.statistics,
            context=certifications.context,
        )

        return CanonicalFeatureCollection(
            skills=sorted_skills,
            experience=sorted_experience,
            education=sorted_education,
            projects=sorted_projects,
            certifications=sorted_certifications,
            statistics=statistics,
            validation_summary=validation_summary,
            metadata=dict(metadata) if metadata else {},
        )
