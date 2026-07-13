"""Builder constructing immutable Feature objects from Certification entities.

Purpose:
    Map Certification entities exactly 1:1 to generic Features, preserving
    all raw data attributes and metadata inside Feature DTO format.
"""

from __future__ import annotations

import datetime
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationEntity
from ats_engine.domain.feature_engineering.common.provenance import build_provenance
from ats_engine.domain.feature_engineering.common.url_mapping import map_custom_url
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureLocation,
    FeatureMetadata,
)


class CertificationFeatureBuilder:
    """Builder producing immutable Feature representations from Certification entities."""

    @classmethod
    def build(
        self,
        entity: CertificationEntity,
        correlation_id: str,
    ) -> Feature:
        """Construct a Feature object wrapping a CertificationEntity.

        Args:
            entity: The CertificationEntity source object.
            correlation_id: Execution tracker identifier.

        Returns:
            The immutable Feature DTO.
        """
        # 1. Establish Feature ID mapping
        feature_id = f"FEAT-CERTIFICATION-{entity.certification_id}"

        # 2. Build Location structures
        locations: list[FeatureLocation] = []

        # 3. Build Provenance
        provenance = build_provenance(
            source_entity_id=entity.certification_id,
            source_entity_type="CERTIFICATION",
            source_section="CERTIFICATIONS",
            matched_rules=entity.matched_rules,
        )

        # 4. Build Metadata
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        metadata = FeatureMetadata(
            creation_timestamp=now_utc,
            extractor_name="CertificationFeatureExtractor",
            version="1.0",
            custom_attributes={
                "confidence_reason": entity.confidence_reason,
                "correlation_id": correlation_id,
            },
        )

        # 5. Compile generic value mapping (Refinement 12)
        generic_value = {
            "certification_name": entity.certification_name,
            "issuing_organization": entity.issuing_organization,
            "credential_id": entity.credential_id_raw,
            "credential_url": map_custom_url(entity.credential_url),
            "issue_date_raw": entity.issue_date_raw,
            "expiration_date_raw": entity.expiration_date_raw,
            "validity_status_raw": entity.validity_status_raw,
            "associated_skill_ids": entity.associated_skill_ids,
            "associated_skills": entity.associated_skills_raw,
            "description": entity.description_raw,
        }

        # 6. Build Feature
        return Feature(
            feature_id=feature_id,
            name=entity.certification_name or "Unknown Certification",
            category=FeatureCategory.CERTIFICATION,  # Strongly typed category
            value=generic_value,
            confidence=entity.confidence,
            locations=tuple(locations),
            provenance=provenance,
            metadata=metadata,
        )
