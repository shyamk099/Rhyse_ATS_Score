"""Builder constructing immutable Feature objects from Skill entities.

Purpose:
    Aggregate duplicate skill occurrences, compute occurrence counts,
    and build individual Feature instances conforming to Book 04 specs.
"""

from __future__ import annotations

import datetime
from typing import Any, Sequence

from ats_engine.domain.entity_extraction.models import ExtractedEntity
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureLocation,
    FeatureMetadata,
    FeatureProvenance,
)


class SkillFeatureBuilder:
    """Builder producing immutable Feature representations from aggregated Skill entities."""

    @classmethod
    def build(
        self,
        skill_value: str,
        occurrences: Sequence[ExtractedEntity],
        correlation_id: str,
    ) -> Feature:
        """Construct a Feature object aggregating duplicate Skill entities.

        Args:
            skill_value: The canonical or raw name of the skill.
            occurrences: Sequence of matching ExtractedEntity records.
            correlation_id: Execution tracker identifier.

        Returns:
            The immutable Feature DTO.
        """
        # 1. Resolve canonical ID if present
        first_occ = occurrences[0]
        skill_id = first_occ.metadata.get("skill_id") or None  # Keep None if absent (Refinement 1)

        # 2. Establish Feature ID mapping
        if skill_id:
            feature_id = f"FEAT-SKILL-{skill_id}"
        else:
            # Deterministic ID using clean raw value, without fabricating "SKL-GENERIC-*"
            normalized_raw_name = skill_value.replace(" ", "_").lower()
            feature_id = f"FEAT-SKILL-RAW-{normalized_raw_name}"

        # 3. Calculate occurrence count (Refinement 2 - purely structural metric)
        occurrence_count = len(occurrences)

        # 4. Map physical locations
        locations: list[FeatureLocation] = []
        for occ in occurrences:
            if occ.location:
                locations.append(
                    FeatureLocation(
                        start_character=occ.location.start_char,
                        end_character=occ.location.end_char,
                    )
                )

        # 5. Build Provenance (Refinement 1 - preserving None)
        # Combine all sections where this skill occurred
        sections_found = sorted(
            list(set(occ.metadata.get("section_type", "UNKNOWN") for occ in occurrences))
        )
        source_section = ", ".join(sections_found) if sections_found else "UNKNOWN"

        provenance = FeatureProvenance(
            source_entity_id=skill_id,  # Preserves None if absent
            source_entity_type="SKILL",
            source_section=source_section,
            source_document=first_occ.metadata.get("document_name"),
            matched_rules=tuple(
                set(occ.metadata.get("confidence_reason", "") for occ in occurrences)
            ),
        )

        # 6. Build Metadata
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        metadata = FeatureMetadata(
            creation_timestamp=now_utc,
            extractor_name="SkillFeatureExtractor",
            version="1.0",
            custom_attributes={
                "occurrence_count": occurrence_count,
                "category": first_occ.metadata.get("category", "unassigned"),
                "is_canonical": skill_id is not None,
                "correlation_id": correlation_id,
            },
        )

        # 7. Build Feature
        # Use average confidence score across occurrences
        avg_confidence = sum(occ.confidence for occ in occurrences) / len(occurrences)

        return Feature(
            feature_id=feature_id,
            name=skill_value,
            category=FeatureCategory.SKILL,
            value=skill_value,
            confidence=avg_confidence,
            locations=tuple(locations),
            provenance=provenance,
            metadata=metadata,
        )
