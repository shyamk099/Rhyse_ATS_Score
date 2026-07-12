"""Document validation and assembly service.

Purpose:
    Orchestrate physical integrity auditing, cross-model consistency checking,
    statistics compiling, and final packaging into a CanonicalDocument.
"""

from __future__ import annotations

import logging

from ats_engine.domain.document_processing.canonical_assembler import CanonicalDocumentAssembler
from ats_engine.domain.document_processing.canonical_builder import CanonicalDocumentBuilder
from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules
from ats_engine.domain.document_processing.consistency_validator import DocumentConsistencyValidator
from ats_engine.domain.document_processing.integrity_validator import DocumentIntegrityValidator
from ats_engine.domain.document_processing.models import NormalizedDocument, RawDocument
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection
from ats_engine.domain.document_processing.statistics_builder import DocumentStatisticsBuilder
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.infrastructure.logging.factory import LoggerFactory


class DocumentValidationService:
    """Orchestrator driving the deterministic validation pipeline to assemble CanonicalDocuments."""

    def __init__(
        self, rules: CanonicalValidationRules, logger: logging.Logger | None = None
    ) -> None:
        """Initialize the service with rules and logger."""
        self._rules = rules
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate_and_assemble(
        self,
        raw_document: RawDocument,
        normalized_document: NormalizedDocument,
        document_layout: DocumentLayout,
        segment_collection: SegmentCollection,
        parser_used: str,
    ) -> CanonicalDocument:
        """Execute integrity audits, consistency validation, and assemble CanonicalDocument.

        Args:
            raw_document: The source RawDocument.
            normalized_document: The NormalizedDocument.
            document_layout: The DocumentLayout.
            segment_collection: The SegmentCollection.
            parser_used: Class name of parser used to extract content.

        Returns:
            The fully validated, immutable CanonicalDocument.

        Raises:
            IntegrityValidationError: If physical structural audits fail.
            ConsistencyValidationError: If cross-model content parity or block links fail.
            StatisticsValidationError: If statistics gathering fails.
            AssemblyValidationError: If final object wrapping fails.
        """
        self._logger.info("canonical_validation_started", extra={"doc_filename": raw_document.filename})

        # 1. Audit structural integrity
        DocumentIntegrityValidator.validate(document_layout, segment_collection, self._rules)

        # 2. Check cross-model consistency
        DocumentConsistencyValidator.validate(
            normalized_document, document_layout, segment_collection, self._rules
        )

        # 3. Gather physical statistics
        statistics = DocumentStatisticsBuilder.build(
            normalized_document, document_layout, segment_collection
        )

        # 4. Compile metadata
        page_numbers = {line.page_number for block in document_layout.blocks for line in block.lines}
        page_count = max(page_numbers) if page_numbers else 1
        
        metadata = CanonicalDocumentBuilder.build_metadata(
            raw_document, page_count, parser_used
        )

        # 5. Package into the immutable contract container
        canonical_doc = CanonicalDocumentAssembler.assemble(
            normalized_document=normalized_document,
            document_layout=document_layout,
            segment_collection=segment_collection,
            metadata=metadata,
            statistics=statistics,
        )

        self._logger.info(
            "canonical_validation_completed",
            extra={
                "canonical_id": canonical_doc.canonical_id,
                "total_segments": statistics.total_segments,
                "total_characters": statistics.total_characters,
            },
        )

        return canonical_doc
