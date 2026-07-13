"""Builder constructing immutable Feature objects from Project entities.

Purpose:
    Map Project entities exactly 1:1 to generic Features, preserving
    all raw data attributes and metadata inside Feature DTO format.
"""

from __future__ import annotations

import datetime
from ats_engine.domain.entity_extraction.project.project_models import ProjectEntity
from ats_engine.domain.feature_engineering.common.provenance import build_provenance
from ats_engine.domain.feature_engineering.common.url_mapping import map_custom_url
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureLocation,
    FeatureMetadata,
)


class ProjectFeatureBuilder:
    """Builder producing immutable Feature representations from Project entities."""

    @classmethod
    def build(
        self,
        entity: ProjectEntity,
        correlation_id: str,
    ) -> Feature:
        """Construct a Feature object wrapping a ProjectEntity.

        Args:
            entity: The ProjectEntity source object.
            correlation_id: Execution tracker identifier.

        Returns:
            The immutable Feature DTO.
        """
        # 1. Establish Feature ID mapping
        feature_id = f"FEAT-PROJECT-{entity.project_id}"

        # 2. Build Location structures
        locations: list[FeatureLocation] = []

        # 3. Build Provenance
        provenance = build_provenance(
            source_entity_id=entity.project_id,
            source_entity_type="PROJECT",
            source_section="PROJECTS",
            matched_rules=entity.matched_rules,
        )

        # 4. Build Metadata
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        metadata = FeatureMetadata(
            creation_timestamp=now_utc,
            extractor_name="ProjectFeatureExtractor",
            version="1.0",
            custom_attributes={
                "confidence_reason": entity.confidence_reason,
                "correlation_id": correlation_id,
            },
        )

        # Serialize technologies cleanly (Refinement 11)
        tech_list = [
            {"raw_name": t.raw_name, "skill_id": t.skill_id}
            for t in entity.technologies
        ]

        # 5. Compile generic value mapping (Refinement 12)
        generic_value = {
            "project_name": entity.project_name,
            "organization": entity.organization,
            "role": entity.role,
            "start_date_raw": entity.start_date_raw,
            "end_date_raw": entity.end_date_raw,
            "duration_raw": entity.duration_raw,
            "technologies": tuple(tech_list),
            "responsibilities": entity.responsibilities,
            "achievements": entity.achievements,
            "repository_urls": map_custom_url(entity.repo_url),
            "demo_urls": map_custom_url(entity.demo_url),
            "location": entity.location_raw,
        }

        # 6. Build Feature
        return Feature(
            feature_id=feature_id,
            name=entity.project_name or "Unknown Project",
            category=FeatureCategory.PROJECT,  # Strongly typed category
            value=generic_value,
            confidence=entity.confidence,
            locations=tuple(locations),
            provenance=provenance,
            metadata=metadata,
        )
