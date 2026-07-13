"""Structural normalization engine for Project features.

Purpose:
    Implement structural whitespace cleaning of Project entities
    reusing the shared text normalization helpers.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectEntity,
    ProjectTechnology,
)
from ats_engine.domain.feature_engineering.common.normalization import normalize_text
from ats_engine.domain.feature_engineering.project.rules import ProjectFeatureRules


class ProjectFeatureNormalizer:
    """Stateless normalizer performing whitespace-level cleaning of extracted project fields."""

    def normalize(self, entity: ProjectEntity, rules: ProjectFeatureRules) -> ProjectEntity:
        """Structurally clean a Project entity copy without altering semantic meanings.

        Args:
            entity: ProjectEntity domain object.
            rules: Active ProjectFeatureRules payload.

        Returns:
            A structurally cleaned copy of the ProjectEntity.
        """
        if not rules.normalize_whitespace:
            return entity

        # Normalize simple string fields
        project_name = normalize_text(entity.project_name)
        organization = normalize_text(entity.organization)
        role = normalize_text(entity.role)
        start_date_raw = normalize_text(entity.start_date_raw)
        end_date_raw = normalize_text(entity.end_date_raw)
        duration_raw = normalize_text(entity.duration_raw)
        project_description = normalize_text(entity.project_description)
        location_raw = normalize_text(entity.location_raw)
        source_text = normalize_text(entity.source_text) or ""

        # Normalize technology names
        technologies = tuple(
            ProjectTechnology(
                raw_name=normalize_name or "",
                skill_id=tech.skill_id,
            )
            for tech in entity.technologies
            if (normalize_name := normalize_text(tech.raw_name)) is not None
        )

        # Normalize list components
        responsibilities = tuple(
            normalize_resp for r in entity.responsibilities
            if (normalize_resp := normalize_text(r)) is not None
        )
        achievements = tuple(
            normalize_ach for a in entity.achievements
            if (normalize_ach := normalize_text(a)) is not None
        )

        return ProjectEntity(
            project_id=entity.project_id,
            project_name=project_name,
            organization=organization,
            role=role,
            start_date_raw=start_date_raw,
            end_date_raw=end_date_raw,
            duration_raw=duration_raw,
            technologies=technologies,
            responsibilities=responsibilities,
            achievements=achievements,
            project_description=project_description,
            repo_url=entity.repo_url,  # Preserved
            demo_url=entity.demo_url,  # Preserved
            location_raw=location_raw,
            confidence=entity.confidence,
            confidence_reason=entity.confidence_reason,
            matched_rules=entity.matched_rules,
            source_segment_ids=entity.source_segment_ids,
            source_text=source_text,
        )
