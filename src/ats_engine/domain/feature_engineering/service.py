"""Public orchestrating service for Feature Engineering.

Purpose:
    Expose the main domain entrypoint to execute feature extraction
    over CanonicalEntityCollection inputs using active rules configurations.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Mapping, Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.factory import FeatureExtractorFactory
from ats_engine.domain.feature_engineering.models import FeatureCollection, FeatureExtractionContext
from ats_engine.domain.feature_engineering.pipeline import FeatureEngineeringPipeline
from ats_engine.domain.feature_engineering.registry import FeatureExtractorRegistry
from ats_engine.infrastructure.logging.factory import LoggerFactory


class FeatureEngineeringService:
    """Primary service coordinating dynamic feature engineering pipeline executions."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize FeatureEngineeringService with internal dependency instances."""
        self._registry = FeatureExtractorRegistry()
        self._factory = FeatureExtractorFactory(self._registry)
        self._pipeline = FeatureEngineeringPipeline()
        self._logger = logger or LoggerFactory.get_logger(__name__)

    @property
    def registry(self) -> FeatureExtractorRegistry:
        """Expose the registry for dynamic extractor registration.

        Returns:
            The FeatureExtractorRegistry instance.
        """
        return self._registry

    @property
    def factory(self) -> FeatureExtractorFactory:
        """Expose the factory.

        Returns:
            The FeatureExtractorFactory instance.
        """
        return self._factory

    def extract_features(
        self,
        canonical_entities: CanonicalEntityCollection,
        enabled_extractors: Sequence[str],
        rules: Mapping[str, Any] | None = None,
    ) -> FeatureCollection:
        """Coordinate registry retrieval and pipeline execution to generate features.

        Args:
            canonical_entities: Consolidated entities input.
            enabled_extractors: Ordered list of string keys representing active extractors.
            rules: Config payload from the Rule Engine.

        Returns:
            An immutable FeatureCollection.
        """
        correlation_id = f"feat_corr_{uuid.uuid4().hex[:12]}"
        self._logger.info(
            "feature_engineering_service_extraction_started",
            extra={"correlation_id": correlation_id, "enabled_count": len(enabled_extractors)},
        )

        # Build execution context
        context = FeatureExtractionContext(
            correlation_id=correlation_id,
            rule_engine_config=rules or {},
        )

        # Resolve extractors in order
        resolved_extractors = []
        for extractor_key in enabled_extractors:
            # Resolves and instantiates dynamically through factory
            extractor = self._factory.get_extractor(extractor_key)
            resolved_extractors.append(extractor)

        # Execute pipeline
        collection = self._pipeline.execute(
            canonical_entities=canonical_entities,
            extractors=resolved_extractors,
            context=context,
        )

        self._logger.info(
            "feature_engineering_service_extraction_completed",
            extra={
                "correlation_id": correlation_id,
                "total_features": len(collection.features),
            },
        )

        return collection
