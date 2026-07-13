"""Structural normalization engine for Skill features.

Purpose:
    Implement structural modifications (trimming, collapsing duplicate spaces)
    without altering canonical values or adding semantic inference.
"""

from __future__ import annotations

import re

from ats_engine.domain.entity_extraction.models import ExtractedEntity
from ats_engine.domain.feature_engineering.skills.rules import SkillFeatureRules


class SkillFeatureNormalizer:
    """Stateless normalizer performing only whitespace-level cleaning of extracted fields."""

    @classmethod
    def normalize_text(cls, text: str) -> str:
        """Trim whitespace and collapse duplicate spaces inside a string.

        Args:
            text: Source string.

        Returns:
            Cleaned string.
        """
        if not text:
            return ""
        # Collapse multiple spaces into a single space, trim margins
        return re.sub(r"\s+", " ", text).strip()

    def normalize(self, entity: ExtractedEntity, rules: SkillFeatureRules) -> ExtractedEntity:
        """Structurally clean a Skill entity copy without altering canonical definitions.

        Args:
            entity: ExtractedEntity domain object.
            rules: Active SkillFeatureRules payload.

        Returns:
            A structurally cleaned copy of the ExtractedEntity.
        """
        if not rules.normalize_whitespace:
            return entity

        # Normalize metadata fields to strip extraneous spacing
        normalized_metadata = {}
        for k, v in entity.metadata.items():
            # Retain non-string attributes if any, but clean string attributes
            normalized_metadata[k] = self.normalize_text(v) if isinstance(v, str) else v

        # Trim value text structurally, preserving raw canonical values
        normalized_value = self.normalize_text(entity.value)

        return ExtractedEntity(
            entity_type=entity.entity_type,
            value=normalized_value,
            confidence=entity.confidence,
            location=entity.location,
            metadata=normalized_metadata,
        )
