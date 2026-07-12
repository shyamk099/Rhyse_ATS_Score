"""Education entity builder.

Purpose:
    Compile assembled education records into final EducationEntity models
    with deterministic confidence scores and explainability reasons.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.education.education_models import (
    AssembledEducation,
    EducationEntity,
)
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules


class EducationEntityBuilder:
    """Stateless builder compiling assembled records into domain EducationEntity models."""

    @classmethod
    def build(
        cls, assembled: AssembledEducation, rules: EducationExtractionRules
    ) -> EducationEntity:
        """Construct an EducationEntity with deterministic confidence and provenance.

        Args:
            assembled: The assembled compound record.
            rules: Configured extraction rules.

        Returns:
            The compiled, immutable EducationEntity.
        """
        matched_rules: list[str] = []
        confidence_components: list[float] = []

        if assembled.institution_name:
            matched_rules.append("institution_indicator_matched")
            confidence_components.append(0.3)

        if assembled.degree:
            matched_rules.append("degree_indicator_matched")
            confidence_components.append(0.3)

        if assembled.start_date_raw or assembled.end_date_raw:
            matched_rules.append("date_detected")
            confidence_components.append(0.15)

        if assembled.graduation_date_raw:
            matched_rules.append("graduation_date_detected")
            confidence_components.append(0.05)

        if assembled.gpa_raw:
            matched_rules.append("gpa_detected")
            confidence_components.append(0.1)

        if assembled.grade_raw:
            matched_rules.append("grade_detected")
            confidence_components.append(0.05)

        if assembled.honors:
            matched_rules.append("honors_detected")
            confidence_components.append(0.05)

        base_confidence = sum(confidence_components) if confidence_components else 0.1

        # Scale by section confidence mapping
        section_confidence = rules.confidence_mappings.get(
            "EDUCATION",
            rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
        )
        confidence = min(
            base_confidence * section_confidence / 0.95, 1.0
        ) if section_confidence else base_confidence

        reason_parts = [f"Matched rules: {', '.join(matched_rules)}"]
        reason_parts.append(f"Component score: {base_confidence:.2f}")
        reason_parts.append(f"Section weight: {section_confidence}")
        confidence_reason = "; ".join(reason_parts)

        return EducationEntity(
            education_id=assembled.education_id,
            institution_name=assembled.institution_name,
            degree=assembled.degree,
            specialization=assembled.specialization,
            field_of_study=assembled.field_of_study,
            start_date_raw=assembled.start_date_raw,
            end_date_raw=assembled.end_date_raw,
            graduation_date_raw=assembled.graduation_date_raw,
            gpa_raw=assembled.gpa_raw,
            grade_raw=assembled.grade_raw,
            honors=assembled.honors,
            certifications=assembled.certifications,
            location_raw=assembled.location_raw,
            confidence=round(confidence, 4),
            confidence_reason=confidence_reason,
            matched_rules=tuple(matched_rules),
            source_segment_ids=assembled.source_segment_ids,
            source_text=assembled.source_text,
        )
