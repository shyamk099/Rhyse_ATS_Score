"""Concrete Project Feature Extractor implementation.

Purpose:
    Coordinate Project entity validation, structural normalization,
    and 1:1 mapping into generic Features.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.models import Feature, FeatureExtractionContext
from ats_engine.domain.feature_engineering.project.builder import ProjectFeatureBuilder
from ats_engine.domain.feature_engineering.project.normalizer import ProjectFeatureNormalizer
from ats_engine.domain.feature_engineering.project.rules import ProjectFeatureRules
from ats_engine.domain.feature_engineering.project.stats_builder import ProjectFeatureStatisticsBuilder
from ats_engine.domain.feature_engineering.project.validator import ProjectFeatureValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ProjectFeatureExtractor(FeatureExtractor):
    """Stateless FeatureExtractor mapping canonical Project entities to generic Features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize extractor with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = ProjectFeatureValidator(self._logger)
        self._normalizer = ProjectFeatureNormalizer()

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        """Transform canonical Project entities into generic Feature objects.

        Args:
            canonical_entities: Consolidated entity collections.
            context: Pipeline execution context.

        Returns:
            A sequence of Project Feature DTOs.
        """
        self._logger.info(
            "project_feature_extraction_started",
            extra={"correlation_id": context.correlation_id},
        )

        # 1. Resolve Rules
        rules_payload = context.rule_engine_config.get("project_feature_rules")
        if isinstance(rules_payload, dict):
            rules = ProjectFeatureRules(**rules_payload)
        else:
            rules = ProjectFeatureRules()

        # Exit immediately if disabled
        if not rules.enabled:
            self._logger.info(
                "project_feature_extraction_disabled",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # Ensure project records exist
        if not canonical_entities.projects or not canonical_entities.projects.entities:
            self._logger.info(
                "project_feature_extraction_empty_input",
                extra={"correlation_id": context.correlation_id},
            )
            return []

        # 2. Validate, Normalize & Build (Exactly 1:1 mapping)
        features: list[Feature] = []
        warnings_count = 0
        tech_count = 0

        for entity in canonical_entities.projects.entities:
            # Run Validation (raises ValueError on threshold failure or required missing fields)
            warnings = self._validator.validate(entity, rules)
            warnings_count += len(warnings)

            if entity.technologies:
                tech_count += 1

            # Run whitespace-level normalization
            normalized_entity = self._normalizer.normalize(entity, rules)

            # Build Feature DTO
            feature = ProjectFeatureBuilder.build(
                entity=normalized_entity,
                correlation_id=context.correlation_id,
            )
            features.append(feature)

        # Calculate metrics
        stats = ProjectFeatureStatisticsBuilder.calculate(
            input_count=len(canonical_entities.projects.entities),
            output_count=len(features),
            warnings_count=warnings_count,
            tech_count=tech_count,
        )

        self._logger.info(
            "project_feature_extraction_completed",
            extra={
                "correlation_id": context.correlation_id,
                "stats": stats,
            },
        )

        return features
