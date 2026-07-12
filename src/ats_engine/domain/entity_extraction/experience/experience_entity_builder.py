"""Experience entity builder.

Purpose:
    Compile assembled experience records into final ExperienceEntity models
    with deterministic confidence scores and explainability reasons.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.experience.experience_models import (
    AssembledExperience,
    ExperienceEntity,
)
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules


class ExperienceEntityBuilder:
    """Stateless builder compiling assembled records into domain ExperienceEntity models."""

    @classmethod
    def build(
        cls, assembled: AssembledExperience, rules: ExperienceExtractionRules
    ) -> ExperienceEntity:
        """Construct an ExperienceEntity with deterministic confidence and provenance.

        Args:
            assembled: The assembled compound record.
            rules: Configured extraction rules.

        Returns:
            The compiled, immutable ExperienceEntity.
        """
        # Calculate deterministic confidence
        matched_rules: list[str] = []
        confidence_components: list[float] = []

        if assembled.company_name:
            matched_rules.append("company_indicator_matched")
            confidence_components.append(0.3)

        if assembled.job_title:
            matched_rules.append("role_indicator_matched")
            confidence_components.append(0.3)

        if assembled.start_date_raw:
            matched_rules.append("start_date_detected")
            confidence_components.append(0.2)

        if assembled.end_date_raw or assembled.is_current:
            matched_rules.append("end_date_or_current_detected")
            confidence_components.append(0.1)

        if assembled.responsibilities:
            matched_rules.append("responsibilities_detected")
            confidence_components.append(0.1)

        base_confidence = sum(confidence_components) if confidence_components else 0.1

        # Scale by section confidence mapping
        section_confidence = rules.confidence_mappings.get(
            "EXPERIENCE",
            rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
        )
        confidence = min(base_confidence * section_confidence / 0.95, 1.0) if section_confidence else base_confidence

        reason_parts = [f"Matched rules: {', '.join(matched_rules)}"]
        reason_parts.append(f"Component score: {base_confidence:.2f}")
        reason_parts.append(f"Section weight: {section_confidence}")
        confidence_reason = "; ".join(reason_parts)

        return ExperienceEntity(
            experience_id=assembled.experience_id,
            company_name=assembled.company_name,
            job_title=assembled.job_title,
            employment_type=assembled.employment_type,
            start_date_raw=assembled.start_date_raw,
            end_date_raw=assembled.end_date_raw,
            is_current=assembled.is_current,
            responsibilities=assembled.responsibilities,
            technologies=assembled.technologies,
            achievements=assembled.achievements,
            confidence=round(confidence, 4),
            confidence_reason=confidence_reason,
            matched_rules=tuple(matched_rules),
            source_segment_ids=assembled.source_segment_ids,
            source_text=assembled.source_text,
        )
