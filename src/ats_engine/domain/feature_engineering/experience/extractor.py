"""Concrete Experience Feature Extractor implementation.

Purpose:
    Coordinate Experience entity validation, structural normalization,
    and 1:1 mapping into generic Features.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.models import Feature, FeatureExtractionContext
from ats_engine.domain.feature_engineering.experience.builder import ExperienceFeatureBuilder
from ats_engine.domain.feature_engineering.experience.normalizer import ExperienceFeatureNormalizer
from ats_engine.domain.feature_engineering.experience.rules import ExperienceFeatureRules
from ats_engine.domain.feature_engineering.experience.stats_builder import ExperienceFeatureStatisticsBuilder
from ats_engine.domain.feature_engineering.experience.validator import ExperienceFeatureValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ExperienceFeatureExtractor(FeatureExtractor):
    """Stateless FeatureExtractor mapping canonical Experience entities to generic Features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize extractor with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = ExperienceFeatureValidator(self._logger)
        self._normalizer = ExperienceFeatureNormalizer()

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        """Transform canonical Experience entities into generic Feature objects.

        Args:
            canonical_entities: Consolidated entity collections.
            context: Pipeline execution context.

        Returns:
            A sequence of Experience Feature DTOs.
        """
        self._logger.info(
            "experience_feature_extraction_started",
            extra={"correlation_id": context.correlation_id},
        )

        # 1. Resolve Rules
        rules_payload = context.rule_engine_config.get("experience_feature_rules")
        if isinstance(rules_payload, dict):
            rules = ExperienceFeatureRules(**rules_payload)
        else:
            rules = ExperienceFeatureRules()

        # Exit immediately if disabled
        if not rules.enabled:
            self._logger.info(
                "experience_feature_extraction_disabled",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # Ensure experiences metadata exists
        if not canonical_entities.experiences or not canonical_entities.experiences.entities:
            self._logger.info(
                "experience_feature_extraction_empty_input",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # 2. Validate, Normalize & Build (Exactly 1:1 mapping - Refinement 3)
        features: list[Feature] = []
        warnings_count = 0
        current_count = 0

        for entity in canonical_entities.experiences.entities:
            # Run Validation (raises ValueError on threshold failure or required missing fields)
            warnings = self._validator.validate(entity, rules)
            warnings_count += len(warnings)

            if entity.is_current:
                current_count += 1

            # Run whitespace-level normalization (Refinement 6)
            normalized_entity = self._normalizer.normalize(entity, rules)

            # Build Feature DTO (Refinement 2 - generic mapping value)
            feature = ExperienceFeatureBuilder.build(
                entity=normalized_entity,
                correlation_id=context.correlation_id,
            )
            features.append(feature)

        # Calculate metrics
        stats = ExperienceFeatureStatisticsBuilder.calculate(
            input_count=len(canonical_entities.experiences.entities),
            output_count=len(features),
            warnings_count=warnings_count,
            current_count=current_count,
        )

        self._logger.info(
            "experience_feature_extraction_completed",
            extra={
                "correlation_id": context.correlation_id,
                "stats": stats,
            },
        )

        return features
