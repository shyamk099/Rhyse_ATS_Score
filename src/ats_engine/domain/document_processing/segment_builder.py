"""Physical segment builder.

Purpose:
    Aggregate contiguous layout blocks into physical segments based on layout size and page rules.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment, SegmentMetadata
from ats_engine.domain.document_processing.segmentation_rules import SegmentationRules
from ats_engine.domain.document_processing.structure_models import PhysicalBlock


class PhysicalSegmentBuilder:
    """Builder grouping sequential blocks into immutable DocumentSegments."""

    @classmethod
    def build_segments(
        cls, blocks: Sequence[PhysicalBlock], rules: SegmentationRules
    ) -> list[DocumentSegment]:
        """Group sequential blocks into segments based on size and page boundaries.

        Args:
            blocks: List of resolved PhysicalBlocks.
            rules: The segmentation parameters.

        Returns:
            A list of constructed DocumentSegment instances.
        """
        if not blocks:
            return []

        segments: list[DocumentSegment] = []
        current_blocks: list[PhysicalBlock] = []
        current_char_count = 0
        current_page: int | None = None
        
        segment_counter = 1

        def flush_current_segment() -> None:
            nonlocal segment_counter
            if not current_blocks:
                return

            seg_id = f"segment_{segment_counter:04d}"
            text_content = "\n\n".join(b.raw_text for b in current_blocks)

            # Determine page range
            pages = [line.page_number for b in current_blocks for line in b.lines]
            page_range = (min(pages), max(pages)) if pages else (1, 1)

            # Map block range using start and end global line numbers
            line_numbers = [line.line_number for b in current_blocks for line in b.lines]
            block_range = (min(line_numbers), max(line_numbers)) if line_numbers else (1, 1)

            total_lines = sum(len(b.lines) for b in current_blocks)

            metadata = SegmentMetadata(
                segment_id=seg_id,
                reading_order=segment_counter,
                page_range=page_range,
                block_range=block_range,
                character_count=len(text_content),
                line_count=total_lines,
            )

            segment = DocumentSegment(
                segment_id=seg_id,
                text_content=text_content,
                metadata=metadata,
                associated_blocks=tuple(current_blocks),
            )
            segments.append(segment)
            segment_counter += 1

        for block in blocks:
            block_chars = len(block.raw_text)
            block_page = block.lines[0].page_number if block.lines else 1

            should_flush = False
            if current_blocks:
                if current_char_count + block_chars > rules.max_segment_characters:
                    should_flush = True
                elif len(current_blocks) >= rules.max_segment_blocks:
                    should_flush = True
                elif rules.split_on_page_transition and block_page != current_page:
                    should_flush = True

            if should_flush:
                flush_current_segment()
                current_blocks = []
                current_char_count = 0

            if not current_blocks:
                current_page = block_page

            current_blocks.append(block)
            current_char_count += block_chars

        flush_current_segment()
        return segments
