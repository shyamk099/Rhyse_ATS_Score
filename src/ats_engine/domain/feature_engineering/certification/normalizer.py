"""Structural normalization engine for Certification features.

Purpose:
    Implement structural whitespace cleaning of Certification entities
    reusing the shared text normalization helpers.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.certification.certification_models import CertificationEntity
from ats_engine.domain.feature_engineering.common.normalization import normalize_text
from ats_engine.domain.feature_engineering.certification.rules import CertificationFeatureRules


class CertificationFeatureNormalizer:
    """Stateless normalizer performing whitespace-level cleaning of extracted certification fields."""

    def normalize(self, entity: CertificationEntity, rules: CertificationFeatureRules) -> CertificationEntity:
        """Structurally clean a Certification entity copy without altering semantic meanings.

        Args:
            entity: CertificationEntity domain object.
            rules: Active CertificationFeatureRules payload.

        Returns:
            A structurally cleaned copy of the CertificationEntity.
        """
        if not rules.normalize_whitespace:
            return entity

        # Normalize simple string fields
        certification_name = normalize_text(entity.certification_name)
        issuing_organization = normalize_text(entity.issuing_organization)
        credential_id_raw = normalize_text(entity.credential_id_raw)
        issue_date_raw = normalize_text(entity.issue_date_raw)
        expiration_date_raw = normalize_text(entity.expiration_date_raw)
        validity_status_raw = normalize_text(entity.validity_status_raw)
        description_raw = normalize_text(entity.description_raw)
        source_text = normalize_text(entity.source_text) or ""

        # Normalize tuple components
        associated_skill_ids = tuple(
            normalize_text(sid) for sid in entity.associated_skill_ids if sid is not None
        )
        associated_skills_raw = tuple(
            normalize_text(sk) for sk in entity.associated_skills_raw if sk is not None
        )

        return CertificationEntity(
            certification_id=entity.certification_id,
            certification_name=certification_name,
            issuing_organization=issuing_organization,
            credential_id_raw=credential_id_raw,
            credential_url=entity.credential_url,  # Preserved
            issue_date_raw=issue_date_raw,
            expiration_date_raw=expiration_date_raw,
            validity_status_raw=validity_status_raw,
            associated_skill_ids=associated_skill_ids,
            associated_skills_raw=associated_skills_raw,
            description_raw=description_raw,
            confidence=entity.confidence,
            confidence_reason=entity.confidence_reason,
            matched_rules=entity.matched_rules,
            source_segment_ids=entity.source_segment_ids,
            source_text=source_text,
        )
