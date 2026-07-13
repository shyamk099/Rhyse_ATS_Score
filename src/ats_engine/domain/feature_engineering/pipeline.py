"""Execution pipeline for Feature Engineering.

Purpose:
    Execute resolved FeatureExtractors sequentially, aggregate features,
    and compute execution performance metrics.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.exceptions import PipelineExecutionError
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCollection,
    FeatureEngineeringStatistics,
    FeatureExtractionContext,
)
from ats_engine.infrastructure.logging.factory import LoggerFactory


class FeatureEngineeringPipeline:
    """Feature-agnostic sequential pipeline running FeatureExtractor instances."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize pipeline with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def execute(
        self,
        canonical_entities: CanonicalEntityCollection,
        extractors: Sequence[FeatureExtractor],
        context: FeatureExtractionContext,
    ) -> FeatureCollection:
        """Run all extractors in sequence, collect stats, and return FeatureCollection.

        Args:
            canonical_entities: Consolidated entities input.
            extractors: Set of resolved, ordered extractor instances.
            context: Context containing rules parameters and tracking fields.

        Returns:
            An immutable FeatureCollection.

        Raises:
            PipelineExecutionError: If any extractor raises an exception.
        """
        self._logger.info(
            "feature_engineering_pipeline_started",
            extra={"correlation_id": context.correlation_id},
        )

        start_time = time.perf_counter()
        features: list[Feature] = []
        extractor_counts: dict[str, int] = {}

        for extractor in extractors:
            extractor_name = extractor.__class__.__name__
            self._logger.info(
                "feature_extractor_execution_started",
                extra={
                    "correlation_id": context.correlation_id,
                    "extractor": extractor_name,
                },
            )

            ext_start = time.perf_counter()
            try:
                extracted_features = extractor.extract(canonical_entities, context)
                features.extend(extracted_features)
                extractor_counts[extractor_name] = len(extracted_features)

                ext_duration = time.perf_counter() - ext_start
                self._logger.info(
                    "feature_extractor_execution_completed",
                    extra={
                        "correlation_id": context.correlation_id,
                        "extractor": extractor_name,
                        "feature_count": len(extracted_features),
                        "duration_seconds": ext_duration,
                    },
                )
            except Exception as exc:
                self._logger.error(
                    "feature_extractor_execution_failed",
                    extra={
                        "correlation_id": context.correlation_id,
                        "extractor": extractor_name,
                        "error_message": str(exc),
                    },
                )
                raise PipelineExecutionError(
                    f"Pipeline extractor '{extractor_name}' failed during execution: {exc}"
                ) from exc

        duration = time.perf_counter() - start_time

        stats = FeatureEngineeringStatistics(
            total_features_extracted=len(features),
            extractor_counts=extractor_counts,
            execution_duration_seconds=duration,
        )

        collection = FeatureCollection(
            features=tuple(features),
            statistics=stats,
            context=context,
        )

        self._logger.info(
            "feature_engineering_pipeline_completed",
            extra={
                "correlation_id": context.correlation_id,
                "total_features": len(features),
                "duration_seconds": duration,
            },
        )

        return collection
