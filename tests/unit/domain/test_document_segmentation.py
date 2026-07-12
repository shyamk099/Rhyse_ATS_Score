"""Unit tests for the Document Segmentation & Reading Order layer.

Purpose:
    Verify natural reading order sorting, size/page-bound segmentation compiling,
    strict structural integrity validation, and model immutability.
"""

from __future__ import annotations

import unittest
from typing import Sequence
from pydantic import ValidationError

from ats_engine.domain.document_processing.exceptions import SegmentValidationError as ProcessingValidationError
from ats_engine.domain.document_processing.structure_models import (
    BlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.segmentation_models import DocumentSegment, SegmentCollection
from ats_engine.domain.document_processing.segmentation_rules import SegmentationRules
from ats_engine.domain.document_processing.reading_order import ReadingOrderResolver
from ats_engine.domain.document_processing.segment_builder import PhysicalSegmentBuilder
from ats_engine.domain.document_processing.segment_validator import SegmentValidator
from ats_engine.domain.document_processing.segmenter import DocumentSegmenter


class DocumentSegmentationTests(unittest.TestCase):
    """Test suite validating stateless block aggregation and sequence checks."""

    def setUp(self) -> None:
        """Initialize segmenter configurations."""
        self._rules = SegmentationRules(
            max_segment_characters=100,
            max_segment_blocks=3,
            split_on_page_transition=True,
        )
        self._segmenter = DocumentSegmenter(self._rules)

    def test_sorts_blocks_into_reading_order(self) -> None:
        """ReadingOrderResolver sorts blocks page-by-page, top-to-bottom."""
        # Unsorted block sequence (page 2 block, followed by page 1 block)
        b1 = self._create_block(BlockType.TEXT, page=2, start_line=10)
        b2 = self._create_block(BlockType.HEADING, page=1, start_line=1)
        
        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)
        sorted_blocks = ReadingOrderResolver.resolve(layout)

        self.assertEqual(b2, sorted_blocks[0])
        self.assertEqual(b1, sorted_blocks[1])

    def test_segments_paragraphs_respecting_character_limits(self) -> None:
        """Builder flushes segment when adding a block exceeds max_segment_characters."""
        # Create blocks: text is length 60 each. Max chars is 100.
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1, text="X" * 60)
        b2 = self._create_block(BlockType.TEXT, page=1, start_line=2, text="Y" * 60)

        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)
        collection = self._segmenter.segment(layout)

        # Expected: split into 2 separate segments because 60 + 60 > 100
        self.assertEqual(2, collection.total_segments)
        self.assertEqual("segment_0001", collection.segments[0].segment_id)
        self.assertEqual("segment_0002", collection.segments[1].segment_id)

    def test_segments_respect_block_limits(self) -> None:
        """Builder flushes segment when block count reaches max_segment_blocks limit."""
        # Max blocks is 3
        blocks = tuple(self._create_block(BlockType.TEXT, page=1, start_line=i, text="A") for i in range(1, 5))
        layout = DocumentLayout(blocks=blocks, total_blocks=4, total_lines=4)
        
        collection = self._segmenter.segment(layout)

        # Expected: segment 1 has 3 blocks, segment 2 has 1 block
        self.assertEqual(2, collection.total_segments)
        self.assertEqual(3, len(collection.segments[0].associated_blocks))
        self.assertEqual(1, len(collection.segments[1].associated_blocks))

    def test_splits_on_page_transitions(self) -> None:
        """Builder flushes segment at page boundary when split_on_page_transition is True."""
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1, text="Page 1 Content")
        b2 = self._create_block(BlockType.TEXT, page=2, start_line=2, text="Page 2 Content")

        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)
        collection = self._segmenter.segment(layout)

        # Split on page transition
        self.assertEqual(2, collection.total_segments)
        self.assertEqual((1, 1), collection.segments[0].metadata.page_range)
        self.assertEqual((2, 2), collection.segments[1].metadata.page_range)

    def test_validator_detects_block_mismatch(self) -> None:
        """SegmentValidator detects if any blocks are missing from segment collection."""
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1)
        b2 = self._create_block(BlockType.TEXT, page=1, start_line=2)
        
        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)

        # Build segments manually omitting b2
        missing_segments = PhysicalSegmentBuilder.build_segments([b1], self._rules)

        with self.assertRaises(ProcessingValidationError):
            SegmentValidator.validate(layout, missing_segments)

    def test_validator_detects_duplicate_blocks(self) -> None:
        """SegmentValidator detects if duplicate blocks are included in segment list."""
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1)
        layout = DocumentLayout(blocks=(b1,), total_blocks=1, total_lines=1)

        # Manually create duplicate block reference list
        seg_meta = SegmentCollection(
            segments=(
                self._create_segment("segment_0001", [b1], index=1),
                self._create_segment("segment_0002", [b1], index=2),
            ),
            total_segments=2,
            total_characters=len(b1.raw_text) * 2,
        )

        with self.assertRaises(ProcessingValidationError):
            SegmentValidator.validate(layout, seg_meta.segments)

    def test_validator_detects_out_of_order_blocks(self) -> None:
        """SegmentValidator detects if blocks violate sequential reading order."""
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1)
        b2 = self._create_block(BlockType.TEXT, page=1, start_line=2)
        
        layout = DocumentLayout(blocks=(b1, b2), total_blocks=2, total_lines=2)

        # Build segments in reverse order with block limit = 1 to force separate segments
        split_rules = SegmentationRules(max_segment_blocks=1)
        reversed_segments = PhysicalSegmentBuilder.build_segments([b2, b1], split_rules)

        with self.assertRaises(ProcessingValidationError):
            SegmentValidator.validate(layout, reversed_segments)

    def test_segment_collection_models_are_immutable(self) -> None:
        """Caller cannot modify fields in compiled segments or metadata."""
        b1 = self._create_block(BlockType.TEXT, page=1, start_line=1)
        layout = DocumentLayout(blocks=(b1,), total_blocks=1, total_lines=1)
        
        collection = self._segmenter.segment(layout)
        
        with self.assertRaises(ValidationError):
            collection.segments[0].metadata.model_validate({"reading_order": 99})

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
        from ats_engine.domain.document_processing.segmentation_models import SegmentMetadata
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
