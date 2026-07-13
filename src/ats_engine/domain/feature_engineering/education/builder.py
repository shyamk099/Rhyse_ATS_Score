"""Builder constructing immutable Feature objects from Education entities.

Purpose:
    Map Education entities exactly 1:1 to generic Features, preserving
    all raw data attributes and metadata inside Feature DTO format.
"""

from __future__ import annotations

import datetime
from ats_engine.domain.entity_extraction.education.education_models import EducationEntity
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureLocation,
    FeatureMetadata,
    FeatureProvenance,
)


class EducationFeatureBuilder:
    """Builder producing immutable Feature representations from Education entities."""

    @classmethod
    def build(
        self,
        entity: EducationEntity,
        correlation_id: str,
    ) -> Feature:
        """Construct a Feature object wrapping an EducationEntity.

        Args:
            entity: The EducationEntity source object.
            correlation_id: Execution tracker identifier.

        Returns:
            The immutable Feature DTO.
        """
        # 1. Establish Feature ID mapping
        feature_id = f"FEAT-EDUCATION-{entity.education_id}"

        # 2. Build Location structures
        locations: list[FeatureLocation] = []

        # 3. Build Provenance (Refinement 4)
        provenance = FeatureProvenance(
            source_entity_id=entity.education_id,
            source_entity_type="EDUCATION",
            source_section="EDUCATION",
            source_document=None,
            matched_rules=entity.matched_rules,
        )

        # 4. Build Metadata
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        metadata = FeatureMetadata(
            creation_timestamp=now_utc,
            extractor_name="EducationFeatureExtractor",
            version="1.0",
            custom_attributes={
                "confidence_reason": entity.confidence_reason,
                "correlation_id": correlation_id,
            },
        )

        # 5. Compile generic value mapping (Refinement 11 & User Key Recommendation)
        generic_value = {
            "institution": entity.institution_name,
            "degree": entity.degree,
            "major": entity.field_of_study,
            "specialization": entity.specialization,
            "start_date_raw": entity.start_date_raw,
            "end_date_raw": entity.end_date_raw,
            "graduation_date_raw": entity.graduation_date_raw,
            "gpa": entity.gpa_raw,
            "grade": entity.grade_raw,
            "honors": entity.honors,
            "certifications": entity.certifications,
            "location": entity.location_raw,
        }

        # 6. Build Feature
        return Feature(
            feature_id=feature_id,
            name=entity.degree or "Unknown Degree",
            category=FeatureCategory.EDUCATION,  # Strongly typed category (Refinement 5)
            value=generic_value,
            confidence=entity.confidence,
            locations=tuple(locations),
            provenance=provenance,
            metadata=metadata,
        )
