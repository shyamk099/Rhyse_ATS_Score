"""Canonical document assembler.

Purpose:
    Expose assembly routines to package document elements into a single CanonicalDocument contract.
"""

from __future__ import annotations

from ats_engine.domain.document_processing.canonical_models import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalStatistics,
)
from ats_engine.domain.document_processing.exceptions import AssemblyValidationError
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection


class CanonicalDocumentAssembler:
    """Stateless assembler compiling sub-models into a CanonicalDocument contract."""

    @classmethod
    def assemble(
        cls,
        normalized_document: NormalizedDocument,
        document_layout: DocumentLayout,
        segment_collection: SegmentCollection,
        metadata: CanonicalMetadata,
        statistics: CanonicalStatistics,
    ) -> CanonicalDocument:
        """Assemble models into the final immutable CanonicalDocument.

        Args:
            normalized_document: The NormalizedDocument.
            document_layout: The DocumentLayout.
            segment_collection: The SegmentCollection.
            metadata: The CanonicalMetadata.
            statistics: The CanonicalStatistics.

        Returns:
            The immutable CanonicalDocument contract.

        Raises:
            AssemblyValidationError: If assembly fails.
        """
        try:
            return CanonicalDocument(
                canonical_id=metadata.canonical_id,
                normalized_document=normalized_document,
                document_layout=document_layout,
                segment_collection=segment_collection,
                metadata=metadata,
                statistics=statistics,
            )
        except Exception as error:
            raise AssemblyValidationError(f"Assembly failed: {error}") from error
