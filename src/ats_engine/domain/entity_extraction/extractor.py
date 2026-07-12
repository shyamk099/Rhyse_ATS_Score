"""Generic entity extractor interface.

Purpose:
    Define the stateless contract protocol for all domain-specific extractors.
"""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.entity_extraction.models import EntityExtractionContext, ExtractedEntity


@runtime_checkable
class EntityExtractor(Protocol):
    """Stateless protocol for implementing generic segment-based extraction routines."""

    def extract(
        self, segment: DocumentSegment, context: EntityExtractionContext
    ) -> Sequence[ExtractedEntity]:
        """Parse text from a single segment and yield structured entities.

        Args:
            segment: The physical DocumentSegment to analyze.
            context: Read-only context containing configuration mappings.

        Returns:
            A sequence of ExtractedEntity objects.
        """
        ...
