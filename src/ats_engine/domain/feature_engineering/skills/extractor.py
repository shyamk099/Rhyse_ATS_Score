"""Concrete Skill Feature Extractor implementation.

Purpose:
    Coordinate Skill entity validation, structural normalization, duplicate
    occurrence grouping, and assembly into generic Features.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.entity_extraction.models import ExtractedEntity
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.models import Feature, FeatureExtractionContext
from ats_engine.domain.feature_engineering.skills.builder import SkillFeatureBuilder
from ats_engine.domain.feature_engineering.skills.normalizer import SkillFeatureNormalizer
from ats_engine.domain.feature_engineering.skills.rules import SkillFeatureRules
from ats_engine.domain.feature_engineering.skills.stats_builder import SkillFeatureStatisticsBuilder
from ats_engine.domain.feature_engineering.skills.validator import SkillFeatureValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SkillFeatureExtractor(FeatureExtractor):
    """Stateless FeatureExtractor mapping canonical Skill entities to generic Features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize extractor with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = SkillFeatureValidator(self._logger)
        self._normalizer = SkillFeatureNormalizer()

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        """Transform canonical Skill entities into generic Feature objects.

        Args:
            canonical_entities: Consolidated entity collections.
            context: Pipeline execution context.

        Returns:
            A sequence of aggregated Skill Feature DTOs.
        """
        self._logger.info(
            "skill_feature_extraction_started",
            extra={"correlation_id": context.correlation_id},
        )

        # 1. Resolve Rules
        rules_payload = context.rule_engine_config.get("skill_feature_rules")
        if isinstance(rules_payload, dict):
            rules = SkillFeatureRules(**rules_payload)
        else:
            rules = SkillFeatureRules()

        # Exit immediately if disabled
        if not rules.enabled:
            self._logger.info(
                "skill_feature_extraction_disabled",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # Ensure canonical_entities.skills exists
        if not canonical_entities.skills or not canonical_entities.skills.entities:
            self._logger.info(
                "skill_feature_extraction_empty_input",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # 2. Validate & Normalize
        validated_entities: list[ExtractedEntity] = []
        warnings_count = 0
        unregistered_count = 0

        for entity in canonical_entities.skills.entities:
            # Run Validation (raises ValueError on strictly invalid details)
            warnings = self._validator.validate(entity, rules)
            warnings_count += len(warnings)

            # Count unregistered raw skills (Refinement 1)
            skill_id = entity.metadata.get("skill_id")
            if not skill_id:
                unregistered_count += 1

            # Run structural normalization (whitespace-level cleaning only)
            normalized_entity = self._normalizer.normalize(entity, rules)
            validated_entities.append(normalized_entity)

        # 3. Group duplicates (Refinement 4 - ONE Feature per canonical skill)
        # Group by skill_id if present, fallback to lowercase raw name to identify raw duplicates
        grouped_occurrences: dict[str, list[ExtractedEntity]] = {}
        for entity in validated_entities:
            skill_id = entity.metadata.get("skill_id")
            group_key = f"ID:{skill_id}" if skill_id else f"RAW:{entity.value.lower()}"
            if group_key not in grouped_occurrences:
                grouped_occurrences[group_key] = []
            grouped_occurrences[group_key].append(entity)

        # 4. Build Feature DTOs
        features: list[Feature] = []
        for group_key, occurrences in grouped_occurrences.items():
            # Retain the exact canonical name supplied (Refinement 3)
            # Use the first occurrence value (which matches canonical name or raw name)
            skill_name = occurrences[0].value
            feature = SkillFeatureBuilder.build(
                skill_value=skill_name,
                occurrences=occurrences,
                correlation_id=context.correlation_id,
            )
            features.append(feature)

        # Calculate metrics
        stats = SkillFeatureStatisticsBuilder.calculate(
            input_count=len(canonical_entities.skills.entities),
            output_count=len(features),
            warnings_count=warnings_count,
            unregistered_count=unregistered_count,
        )

        self._logger.info(
            "skill_feature_extraction_completed",
            extra={
                "correlation_id": context.correlation_id,
                "stats": stats,
            },
        )

        return features
