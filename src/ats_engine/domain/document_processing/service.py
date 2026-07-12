"""Service orchestrating document parsing, text cleaning, and statistics logging.

Purpose:
    Expose a clean public interface to convert raw document paths into validated ParsingResults.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from ats_engine.domain.document_processing.factory import DocumentParserFactory
from ats_engine.domain.document_processing.models import (
    DocumentMetadata,
    NormalizedDocument,
    ParsingResult,
)
from ats_engine.domain.document_processing.normalization import TextNormalizer
from ats_engine.infrastructure.logging.factory import LoggerFactory


class DocumentProcessingService:
    """Service orchestrating the signature detection, raw parsing, and text normalization pipeline."""

    def __init__(
        self,
        factory: DocumentParserFactory,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the document processing service with a parser factory."""
        self._factory = factory
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def parse(self, file_path: Path | str) -> ParsingResult:
        """Parse raw content from a document file path and return a validated ParsingResult.

        Args:
            file_path: The absolute path to the file.

        Returns:
            An immutable ParsingResult structure.

        Raises:
            DocumentReadError: If the file is unreadable or missing.
            UnsupportedFormatError: If the file signature cannot be parsed.
            CorruptedDocumentError: If the document is corrupted.
            NormalizationError: If the normalization steps fail.
        """
        path = Path(file_path)
        start_time = time.perf_counter()
        
        self._logger.info("document_processing_started", extra={"doc_filename": path.name})

        # 1. Resolve parser stateless instance via signature checks
        parser = self._factory.get_parser(path)

        # 2. Extract raw contents
        raw_doc = parser.parse(path)

        # 3. Clean and normalize content via standalone pipeline
        cleaned_text = TextNormalizer.normalize(raw_doc.raw_content)

        # 4. Generate document statistics
        lines = [line for line in cleaned_text.split("\n") if line.strip()]
        line_count = len(lines)

        paragraphs = [para for para in cleaned_text.split("\n\n") if para.strip()]
        paragraph_count = len(paragraphs)

        char_count = len(cleaned_text)

        normalized_doc = NormalizedDocument(
            cleaned_content=cleaned_text,
            paragraph_count=paragraph_count,
            line_count=line_count,
            char_count=char_count,
        )

        duration = time.perf_counter() - start_time

        metadata = DocumentMetadata(
            file_size_bytes=raw_doc.file_size_bytes,
            page_count=len(raw_doc.pages),
            character_count=char_count,
            line_count=line_count,
            paragraph_count=paragraph_count,
            extraction_duration_seconds=duration,
            parser_used=parser.__class__.__name__,
            encoding="utf-8",
        )

        self._logger.info(
            "document_processing_completed",
            extra={
                "doc_filename": path.name,
                "duration_seconds": duration,
                "character_count": char_count,
                "parser_used": parser.__class__.__name__,
            },
        )

        return ParsingResult(
            raw_document=raw_doc,
            normalized_document=normalized_doc,
            metadata=metadata,
        )
