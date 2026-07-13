"""Shared feature provenance compilation helper.

Purpose:
    Provide consistent instantiation for FeatureProvenance tracking models.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.feature_engineering.models import FeatureProvenance


def build_provenance(
    source_entity_id: str | None,
    source_entity_type: str,
    source_section: str | None = None,
    source_document: str | None = None,
    matched_rules: Sequence[str] = (),
) -> FeatureProvenance:
    """Construct a clean, immutable FeatureProvenance object.

    Args:
        source_entity_id: Canonical record ID.
        source_entity_type: Type label (e.g. PROJECT, CERTIFICATION).
        source_section: Section label of document where matched.
        source_document: Source document filename coordinate.
        matched_rules: Sequence of rule strings applied during pipeline.

    Returns:
        The instantiated FeatureProvenance model.
    """
    return FeatureProvenance(
        source_entity_id=source_entity_id,
        source_entity_type=source_entity_type,
        source_section=source_section,
        source_document=source_document,
        matched_rules=tuple(set(matched_rules)),
    )
