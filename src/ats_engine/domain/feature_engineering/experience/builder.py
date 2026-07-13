"""Builder constructing immutable Feature objects from Experience entities.

Purpose:
    Map Experience entities exactly 1:1 to generic Features, preserving
    all raw data attributes and metadata inside Feature DTO format.
"""

from __future__ import annotations

import datetime
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceEntity
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureLocation,
    FeatureMetadata,
    FeatureProvenance,
)


class ExperienceFeatureBuilder:
    """Builder producing immutable Feature representations from Experience entities."""

    @classmethod
    def build(
        self,
        entity: ExperienceEntity,
        correlation_id: str,
    ) -> Feature:
        """Construct a Feature object wrapping an ExperienceEntity.

        Args:
            entity: The ExperienceEntity source object.
            correlation_id: Execution tracker identifier.

        Returns:
            The immutable Feature DTO.
        """
        # 1. Establish Feature ID mapping
        feature_id = f"FEAT-EXPERIENCE-{entity.experience_id}"

        # 2. Build Location structures (using segment IDs as source section coordinates)
        locations: list[FeatureLocation] = []
        # Since physical offsets are in the extraction pipeline, we represent them dynamically
        # or map segment indexes as locations if page references aren't raw integer fields.

        # 3. Build Provenance (Refinement 4)
        provenance = FeatureProvenance(
            source_entity_id=entity.experience_id,
            source_entity_type="EXPERIENCE",
            source_section="EXPERIENCE",
            source_document=None,  # Derived dynamically when context tracks document namespaces
            matched_rules=entity.matched_rules,
        )

        # 4. Build Metadata
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        metadata = FeatureMetadata(
            creation_timestamp=now_utc,
            extractor_name="ExperienceFeatureExtractor",
            version="1.0",
            custom_attributes={
                "confidence_reason": entity.confidence_reason,
                "correlation_id": correlation_id,
            },
        )

        # 5. Compile generic value mapping (Refinement 2)
        # Holds structured experience data inside generic value DTO
        generic_value = {
            "company": entity.company_name,
            "job_title": entity.job_title,
            "employment_type": entity.employment_type,
            "start_date_raw": entity.start_date_raw,
            "end_date_raw": entity.end_date_raw,
            "is_current": entity.is_current,
            "responsibilities": entity.responsibilities,
            "technologies": entity.technologies,
            "achievements": entity.achievements,
        }

        # 6. Build Feature
        return Feature(
            feature_id=feature_id,
            name=entity.job_title or "Unknown Title",
            category=FeatureCategory.EXPERIENCE,  # Strongly typed category (Refinement 1)
            value=generic_value,
            confidence=entity.confidence,
            locations=tuple(locations),
            provenance=provenance,
            metadata=metadata,
        )
