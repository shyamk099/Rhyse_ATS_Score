"""Segment structural integrity validator.

Purpose:
    Perform verification checks on the output segments to guarantee that no physical blocks
    are duplicated, dropped, or reordered.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.exceptions import SegmentValidationError as ProcessingValidationError
from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.document_processing.structure_models import DocumentLayout, PhysicalBlock


class SegmentValidator:
    """Validator auditing block associations, page boundaries, and reading sequence."""

    @classmethod
    def validate(cls, layout: DocumentLayout, segments: Sequence[DocumentSegment]) -> None:
        """Validate structural integrity of the segments against the source layout.

        Args:
            layout: The original DocumentLayout.
            segments: The built sequence of DocumentSegments.

        Raises:
            RuleValidationError: If any block is missing, duplicated, or out of reading order.
        """
        original_blocks = list(layout.blocks)
        segmented_blocks: list[PhysicalBlock] = []

        for segment in segments:
            for block in segment.associated_blocks:
                segmented_blocks.append(block)

        # 1. Verify block counts match
        if len(original_blocks) != len(segmented_blocks):
            raise ProcessingValidationError(
                f"Block count mismatch: Layout contains {len(original_blocks)} blocks, "
                f"but segments contain {len(segmented_blocks)} blocks."
            )

        # 2. Check for missing, duplicates, or extra blocks
        original_keys = {cls._get_block_key(b) for b in original_blocks}
        segmented_keys: list[str] = []
        
        for block in segmented_blocks:
            key = cls._get_block_key(block)
            if key in segmented_keys:
                raise ProcessingValidationError(f"Duplicate block detected in segment collection: {key}")
            segmented_keys.append(key)

        segmented_keys_set = set(segmented_keys)
        
        missing_keys = original_keys - segmented_keys_set
        if missing_keys:
            raise ProcessingValidationError(f"Blocks missing from segment collection: {missing_keys}")

        extra_keys = segmented_keys_set - original_keys
        if extra_keys:
            raise ProcessingValidationError(f"Extra unregistered blocks in segment collection: {extra_keys}")

        # 3. Verify reading order and page sequence are preserved
        last_line_num = 0
        last_page_num = 0
        
        for segment in segments:
            start_line, end_line = segment.metadata.block_range
            start_page, end_page = segment.metadata.page_range

            if start_line <= last_line_num:
                raise ProcessingValidationError(
                    f"Reading order violation: Segment starts at line {start_line} "
                    f"but preceding segment ended at line {last_line_num}."
                )
            if start_page < last_page_num:
                raise ProcessingValidationError(
                    f"Page order violation: Segment page range {start_page}-{end_page} "
                    f"violates sequence of preceding page {last_page_num}."
                )

            last_line_num = end_line
            last_page_num = end_page

    @classmethod
    def _get_block_key(cls, block: PhysicalBlock) -> str:
        if not block.lines:
            return "empty_block"
        first_line = block.lines[0]
        return f"{first_line.page_number}_{first_line.line_number}"
