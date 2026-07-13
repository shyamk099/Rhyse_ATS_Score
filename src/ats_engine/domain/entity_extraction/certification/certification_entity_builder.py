"""Certification entity builder.

Purpose:
    Compile assembled certification records into final CertificationEntity models
    with deterministic confidence scores and explainability reasons.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.certification.certification_models import (
    AssembledCertification,
    CertificationEntity,
)
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules


class CertificationEntityBuilder:
    """Stateless builder compiling assembled records into domain CertificationEntity models."""

    @classmethod
    def build(
        cls, assembled: AssembledCertification, rules: CertificationExtractionRules
    ) -> CertificationEntity:
        """Construct a CertificationEntity with deterministic confidence and provenance.

        Args:
            assembled: The assembled compound record.
            rules: Configured extraction rules.

        Returns:
            The compiled, immutable CertificationEntity.
        """
        matched_rules: list[str] = []
        confidence_components: list[float] = []

        if assembled.certification_name:
            matched_rules.append("certification_name_indicator_matched")
            confidence_components.append(0.35)

        if assembled.issuing_organization:
            matched_rules.append("issuing_organization_matched")
            confidence_components.append(0.25)

        if assembled.issue_date_raw:
            matched_rules.append("issue_date_detected")
            confidence_components.append(0.15)

        if assembled.expiration_date_raw:
            matched_rules.append("expiration_date_detected")
            confidence_components.append(0.05)

        if assembled.credential_id_raw:
            matched_rules.append("credential_id_detected")
            confidence_components.append(0.1)

        if assembled.credential_url:
            matched_rules.append("credential_url_detected")
            confidence_components.append(0.05)

        if assembled.associated_skill_ids or assembled.associated_skills_raw:
            matched_rules.append("skills_detected")
            confidence_components.append(0.05)

        base_confidence = sum(confidence_components) if confidence_components else 0.1

        # Scale by section confidence mapping
        section_confidence = rules.confidence_mappings.get(
            "CERTIFICATIONS",
            rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
        )
        confidence = min(
            base_confidence * section_confidence / 0.95, 1.0
        ) if section_confidence else base_confidence

        reason_parts = [f"Matched rules: {', '.join(matched_rules)}"]
        reason_parts.append(f"Component score: {base_confidence:.2f}")
        reason_parts.append(f"Section weight: {section_confidence}")
        confidence_reason = "; ".join(reason_parts)

        return CertificationEntity(
            certification_id=assembled.certification_id,
            certification_name=assembled.certification_name,
            issuing_organization=assembled.issuing_organization,
            credential_id_raw=assembled.credential_id_raw,
            credential_url=assembled.credential_url,
            issue_date_raw=assembled.issue_date_raw,
            expiration_date_raw=assembled.expiration_date_raw,
            validity_status_raw=assembled.validity_status_raw,
            associated_skill_ids=assembled.associated_skill_ids,
            associated_skills_raw=assembled.associated_skills_raw,
            description_raw=assembled.description_raw,
            confidence=round(confidence, 4),
            confidence_reason=confidence_reason,
            matched_rules=tuple(matched_rules),
            source_segment_ids=assembled.source_segment_ids,
            source_text=assembled.source_text,
        )
