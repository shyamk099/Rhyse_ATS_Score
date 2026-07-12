"""Unit tests for the Canonical Document Validation layer.

Purpose:
    Verify integrity auditing, content consistency, statistics building, metadata assembling,
    rule engine thresholds integration, and strict exception boundaries.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.document_processing.exceptions import (
    ConsistencyValidationError,
    IntegrityValidationError,
)
from ats_engine.domain.document_processing.models import NormalizedDocument, RawDocument
from ats_engine.domain.document_processing.structure_models import (
    BlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.segmentation_models import (
    DocumentSegment,
    SegmentCollection,
    SegmentMetadata,
)
from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules
from ats_engine.domain.document_processing.validation_service import DocumentValidationService


class CanonicalValidationTests(unittest.TestCase):
    """Test suite validating the structural layout validation and assembly pipeline."""

    def setUp(self) -> None:
        """Initialize validation service and mock data generators."""
        self._rules = CanonicalValidationRules()
        self._service = DocumentValidationService(self._rules)

    def test_assembles_valid_canonical_document(self) -> None:
        """Service executes deterministic pipeline and compiles valid CanonicalDocument."""
        raw_doc, norm_doc, layout, segments = self._create_valid_document_bundle(
            text="Valid test content.", page=1
        )

        canonical_doc = self._service.validate_and_assemble(
            raw_document=raw_doc,
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            parser_used="PdfDocumentParser",
        )

        self.assertIsInstance(canonical_doc, CanonicalDocument)
        self.assertEqual("Valid test content.", canonical_doc.normalized_document.cleaned_content)
        self.assertEqual(1, canonical_doc.statistics.total_segments)
        self.assertEqual(1, canonical_doc.statistics.total_blocks)
        self.assertEqual("PdfDocumentParser", canonical_doc.metadata.parser_used)

    def test_integrity_fails_on_empty_layout(self) -> None:
        """Integrity validation raises IntegrityValidationError when layout blocks are empty."""
        raw_doc, norm_doc, layout, segments = self._create_valid_document_bundle(
            text="Content", page=1
        )
        # Corrupt layout to have zero blocks
        empty_layout = DocumentLayout(blocks=(), total_blocks=0, total_lines=0)

        with self.assertRaises(IntegrityValidationError):
            self._service.validate_and_assemble(
                raw_doc, norm_doc, empty_layout, segments, "PdfDocumentParser"
            )

    def test_integrity_fails_on_page_sequence_gaps(self) -> None:
        """Integrity validation raises IntegrityValidationError when page indexes are non-sequential."""
        # Create blocks on page 1 and page 3 (gap on page 2)
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1, text="P1")
        b2 = self._create_block(BlockType.TEXT, page=3, start_line=2, text="P3")

        raw_doc = RawDocument(filename="doc.pdf", file_size_bytes=10, raw_content="P1\nP3", pages=("P1", "", "P3"))
        norm_doc = NormalizedDocument(cleaned_content="P1\nP3", paragraph_count=2, line_count=2, char_count=5)
        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)

        s1 = self._create_segment("segment_0001", [b1], index=1)
        s2 = self._create_segment("segment_0002", [b2], index=2)
        segments = SegmentCollection(segments=(s1, s2), total_segments=2, total_characters=4)

        with self.assertRaises(IntegrityValidationError):
            self._service.validate_and_assemble(
                raw_doc, norm_doc, layout, segments, "PdfDocumentParser"
            )

    def test_consistency_fails_on_character_mismatch(self) -> None:
        """Consistency validation raises ConsistencyValidationError if normalized content differs from segment text."""
        raw_doc, norm_doc, layout, segments = self._create_valid_document_bundle(
            text="Valid test content.", page=1
        )
        
        # Corrupt normalized document to have mismatched content characters
        mismatched_norm = NormalizedDocument(
            cleaned_content="Completely different content characters",
            paragraph_count=1,
            line_count=1,
            char_count=39,
        )

        with self.assertRaises(ConsistencyValidationError):
            self._service.validate_and_assemble(
                raw_doc, mismatched_norm, layout, segments, "PdfDocumentParser"
            )

    def test_respects_custom_tolerance_rules(self) -> None:
        """Allowed character variance tolerance resolves formatting character mismatches when enabled."""
        raw_doc, norm_doc, layout, segments = self._create_valid_document_bundle(
            text="Content text long enough now", page=1
        )

        # Force a small character difference in normalized text
        mismatched_norm = NormalizedDocument(
            cleaned_content="Content text long enough nowExtra",  # longer
            paragraph_count=1,
            line_count=1,
            char_count=33,
        )

        # Default rules has enable_variance_tolerance = False, so it must fail
        with self.assertRaises(ConsistencyValidationError):
            self._service.validate_and_assemble(
                raw_doc, mismatched_norm, layout, segments, "PdfDocumentParser"
            )

        # Enable tolerance in custom rules
        custom_rules = CanonicalValidationRules(
            allowable_character_count_variance=0.5,
            enable_variance_tolerance=True,
        )
        custom_service = DocumentValidationService(custom_rules)

        # Must pass successfully now
        canonical_doc = custom_service.validate_and_assemble(
            raw_doc, mismatched_norm, layout, segments, "PdfDocumentParser"
        )
        self.assertIsInstance(canonical_doc, CanonicalDocument)

    def test_models_are_immutable(self) -> None:
        """CanonicalDocument models are frozen preventing attribute mutation."""
        raw_doc, norm_doc, layout, segments = self._create_valid_document_bundle(
            text="Content text long enough now", page=1
        )
        canonical_doc = self._service.validate_and_assemble(
            raw_doc, norm_doc, layout, segments, "PdfDocumentParser"
        )

        with self.assertRaises(ValidationError):
            canonical_doc.metadata.model_validate({"encoding": "ascii"})

    def _create_valid_document_bundle(
        self, text: str, page: int
    ) -> tuple[RawDocument, NormalizedDocument, DocumentLayout, SegmentCollection]:
        block = self._create_block(BlockType.TEXT, page=page, start_line=1, text=text)
        
        raw_doc = RawDocument(
            filename="doc.pdf",
            file_size_bytes=100,
            raw_content=text,
            pages=(text,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=text,
            paragraph_count=1,
            line_count=1,
            char_count=len(text),
        )
        layout = DocumentLayout(
            blocks=(block,),
            total_blocks=1,
            total_lines=1,
        )
        segment = self._create_segment("segment_0001", [block], index=1)
        segments = SegmentCollection(
            segments=(segment,),
            total_segments=1,
            total_characters=len(text),
        )
        return raw_doc, norm_doc, layout, segments

    def _create_block(self, block_type: BlockType, page: int, start_line: int, text: str = "text") -> PhysicalBlock:
        line = PhysicalLine(
            text=text,
            line_number=start_line,
            page_number=page,
            indentation_spaces=0,
            character_count=len(text),
        )
        return PhysicalBlock(
            block_type=block_type,
            lines=(line,),
            raw_text=text,
        )

    def _create_segment(self, segment_id: str, blocks: list[PhysicalBlock], index: int) -> DocumentSegment:
        text_content = "\n\n".join(b.raw_text for b in blocks)
        pages = [line.page_number for b in blocks for line in b.lines]
        page_range = (min(pages), max(pages))
        line_numbers = [line.line_number for b in blocks for line in b.lines]
        block_range = (min(line_numbers), max(line_numbers))
        
        metadata = SegmentMetadata(
            segment_id=segment_id,
            reading_order=index,
            page_range=page_range,
            block_range=block_range,
            character_count=len(text_content),
            line_count=sum(len(b.lines) for b in blocks),
        )
        return DocumentSegment(
            segment_id=segment_id,
            text_content=text_content,
            metadata=metadata,
            associated_blocks=tuple(blocks),
        )
