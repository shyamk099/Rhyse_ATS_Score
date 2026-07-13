"""Project entity builder.

Purpose:
    Compile assembled project records into final ProjectEntity models
    with deterministic confidence scores and explainability reasons.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.project.project_models import (
    AssembledProject,
    ProjectEntity,
)
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules


class ProjectEntityBuilder:
    """Stateless builder compiling assembled records into domain ProjectEntity models."""

    @classmethod
    def build(
        cls, assembled: AssembledProject, rules: ProjectExtractionRules
    ) -> ProjectEntity:
        """Construct a ProjectEntity with deterministic confidence and provenance.

        Args:
            assembled: The assembled compound record.
            rules: Configured extraction rules.

        Returns:
            The compiled, immutable ProjectEntity.
        """
        matched_rules: list[str] = []
        confidence_components: list[float] = []

        if assembled.project_name:
            matched_rules.append("project_name_indicator_matched")
            confidence_components.append(0.3)

        if assembled.role:
            matched_rules.append("role_indicator_matched")
            confidence_components.append(0.2)

        if assembled.organization:
            matched_rules.append("organization_indicator_matched")
            confidence_components.append(0.1)

        if assembled.start_date_raw or assembled.end_date_raw:
            matched_rules.append("date_detected")
            confidence_components.append(0.1)

        if assembled.repo_url:
            matched_rules.append("repository_url_detected")
            confidence_components.append(0.15)

        if assembled.demo_url:
            matched_rules.append("demo_url_detected")
            confidence_components.append(0.05)

        if assembled.technologies:
            matched_rules.append("technologies_detected")
            confidence_components.append(0.1)

        base_confidence = sum(confidence_components) if confidence_components else 0.1

        # Scale by section confidence mapping
        section_confidence = rules.confidence_mappings.get(
            "PROJECTS",
            rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
        )
        confidence = min(
            base_confidence * section_confidence / 0.95, 1.0
        ) if section_confidence else base_confidence

        reason_parts = [f"Matched rules: {', '.join(matched_rules)}"]
        reason_parts.append(f"Component score: {base_confidence:.2f}")
        reason_parts.append(f"Section weight: {section_confidence}")
        confidence_reason = "; ".join(reason_parts)

        # Map to mock line numbers/offsets for provenance representation
        source_line_numbers = (1,)  # Mocked line representation
        character_offsets = (0, len(assembled.source_text))

        return ProjectEntity(
            project_id=assembled.project_id,
            project_name=assembled.project_name,
            organization=assembled.organization,
            role=assembled.role,
            start_date_raw=assembled.start_date_raw,
            end_date_raw=assembled.end_date_raw,
            duration_raw=assembled.duration_raw,
            technologies=assembled.technologies,
            responsibilities=assembled.responsibilities,
            achievements=assembled.achievements,
            project_description=assembled.project_description,
            repo_url=assembled.repo_url,
            demo_url=assembled.demo_url,
            location_raw=assembled.location_raw,
            confidence=round(confidence, 4),
            confidence_reason=confidence_reason,
            matched_rules=tuple(matched_rules),
            source_segment_ids=assembled.source_segment_ids,
            source_text=assembled.source_text,
        )
