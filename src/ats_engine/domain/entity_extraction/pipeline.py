"""Entity extraction execution pipeline.

Purpose:
    Coordinate sequential execution of stateless extractors over physical document segments.
"""

from __future__ import annotations

import time
from typing import Sequence

from ats_engine.domain.entity_extraction.exceptions import PipelineExecutionError
from ats_engine.domain.entity_extraction.factory import EntityExtractorFactory
from ats_engine.domain.entity_extraction.models import (
    EntityCollection,
    EntityExtractionContext,
    EntityExtractionStatistics,
    ExtractedEntity,
)


class EntityExtractionPipeline:
    """Stateless pipeline resolving and executing extractors on document segment collections."""

    def __init__(self, factory: EntityExtractorFactory) -> None:
        """Initialize the pipeline with an extractor factory."""
        self._factory = factory

    def execute(
        self,
        context: EntityExtractionContext,
        extractor_types: Sequence[str],
    ) -> EntityCollection:
        """Resolve extractors and run extraction sequentially over document segments.

        Args:
            context: Read-only EntityExtractionContext containing source documents and configs.
            extractor_types: List of extractor type keys to execute.

        Returns:
            An aggregated, immutable EntityCollection container.

        Raises:
            PipelineExecutionError: If any extractor fails or resolution fails.
        """
        start_time = time.perf_counter()

        # 1. Resolve all extractors via factory lookups
        resolved_extractors = []
        for etype in extractor_types:
            try:
                extractor = self._factory.get_extractor(etype)
                resolved_extractors.append((etype, extractor))
            except Exception as error:
                raise PipelineExecutionError(
                    f"Failed to resolve extractor type '{etype}': {error}"
                ) from error

        # 2. Sequentially execute extractors independently over segments
        entities_list: list[ExtractedEntity] = []
        extractor_counts: dict[str, int] = {etype: 0 for etype, _ in resolved_extractors}
        
        segments = context.canonical_document.segment_collection.segments

        for etype, extractor in resolved_extractors:
            for segment in segments:
                try:
                    extracted = extractor.extract(segment, context)
                    for entity in extracted:
                        entities_list.append(entity)
                        extractor_counts[etype] += 1
                except Exception as error:
                    raise PipelineExecutionError(
                        f"Extractor '{etype}' encountered an exception on segment '{segment.segment_id}': {error}"
                    ) from error

        duration = time.perf_counter() - start_time

        statistics = EntityExtractionStatistics(
            extractor_counts=extractor_counts,
            total_entities=len(entities_list),
            execution_duration_seconds=duration,
        )

        return EntityCollection(
            entities=tuple(entities_list),
            statistics=statistics,
        )
