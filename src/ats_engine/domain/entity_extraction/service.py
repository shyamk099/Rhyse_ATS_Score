"""Entity extraction coordination service.

Purpose:
    Expose a unified service interface to run multiple extractors on a CanonicalDocument.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Mapping, Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.models import EntityCollection, EntityExtractionContext
from ats_engine.domain.entity_extraction.pipeline import EntityExtractionPipeline
from ats_engine.infrastructure.logging.factory import LoggerFactory


class EntityExtractionService:
    """Service orchestrating execution contexts, telemetry logs, and pipeline runs."""

    def __init__(
        self,
        pipeline: EntityExtractionPipeline,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize service with pipeline and optional logger dependencies."""
        self._pipeline = pipeline
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract(
        self,
        document: CanonicalDocument,
        extractor_types: Sequence[str],
        rule_engine_config: Mapping[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> EntityCollection:
        """Create execution context and run entity extraction pipeline.

        Args:
            document: The CanonicalDocument to process.
            extractor_types: Names of registered extractors to execute.
            rule_engine_config: Rule configurations from the Rule Engine.
            correlation_id: Optional tracking identifier.

        Returns:
            An immutable EntityCollection.

        Raises:
            PipelineExecutionError: If execution fails.
        """
        cid = correlation_id or f"corr_{uuid.uuid4().hex[:12]}"

        self._logger.info(
            "entity_extraction_started",
            extra={
                "canonical_id": document.canonical_id,
                "correlation_id": cid,
                "extractor_types": list(extractor_types),
            },
        )

        context = EntityExtractionContext(
            canonical_document=document,
            correlation_id=cid,
            rule_engine_config=rule_engine_config or {},
        )

        collection = self._pipeline.execute(context, extractor_types)

        self._logger.info(
            "entity_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "correlation_id": cid,
                "total_entities": collection.statistics.total_entities,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
