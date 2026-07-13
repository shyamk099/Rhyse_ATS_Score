"""Concrete Education Feature Extractor implementation.

Purpose:
    Coordinate Education entity validation, structural normalization,
    and 1:1 mapping into generic Features.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.models import Feature, FeatureExtractionContext
from ats_engine.domain.feature_engineering.education.builder import EducationFeatureBuilder
from ats_engine.domain.feature_engineering.education.normalizer import EducationFeatureNormalizer
from ats_engine.domain.feature_engineering.education.rules import EducationFeatureRules
from ats_engine.domain.feature_engineering.education.stats_builder import EducationFeatureStatisticsBuilder
from ats_engine.domain.feature_engineering.education.validator import EducationFeatureValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class EducationFeatureExtractor(FeatureExtractor):
    """Stateless FeatureExtractor mapping canonical Education entities to generic Features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize extractor with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = EducationFeatureValidator(self._logger)
        self._normalizer = EducationFeatureNormalizer()

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        """Transform canonical Education entities into generic Feature objects.

        Args:
            canonical_entities: Consolidated entity collections.
            context: Pipeline execution context.

        Returns:
            A sequence of Education Feature DTOs.
        """
        self._logger.info(
            "education_feature_extraction_started",
            extra={"correlation_id": context.correlation_id},
        )

        # 1. Resolve Rules
        rules_payload = context.rule_engine_config.get("education_feature_rules")
        if isinstance(rules_payload, dict):
            rules = EducationFeatureRules(**rules_payload)
        else:
            rules = EducationFeatureRules()

        # Exit immediately if disabled
        if not rules.enabled:
            self._logger.info(
                "education_feature_extraction_disabled",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # Ensure education records exist
        if not canonical_entities.education or not canonical_entities.education.entities:
            self._logger.info(
                "education_feature_extraction_empty_input",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # 2. Validate, Normalize & Build (Exactly 1:1 mapping - Refinement 3)
        features: list[Feature] = []
        warnings_count = 0
        degree_count = 0

        for entity in canonical_entities.education.entities:
            # Run Validation (raises ValueError on threshold failure or required missing fields)
            warnings = self._validator.validate(entity, rules)
            warnings_count += len(warnings)

            if entity.degree:
                degree_count += 1

            # Run whitespace-level normalization (Refinement 6)
            normalized_entity = self._normalizer.normalize(entity, rules)

            # Build Feature DTO (Refinement 11 - generic mapping value)
            feature = EducationFeatureBuilder.build(
                entity=normalized_entity,
                correlation_id=context.correlation_id,
            )
            features.append(feature)

        # Calculate metrics
        stats = EducationFeatureStatisticsBuilder.calculate(
            input_count=len(canonical_entities.education.entities),
            output_count=len(features),
            warnings_count=warnings_count,
            degree_count=degree_count,
        )

        self._logger.info(
            "education_feature_extraction_completed",
            extra={
                "correlation_id": context.correlation_id,
                "stats": stats,
            },
        )

        return features
