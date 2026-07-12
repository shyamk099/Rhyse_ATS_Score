"""Reading order resolver.

Purpose:
    Sort physical blocks to match the natural top-to-bottom reading sequence.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.structure_models import DocumentLayout, PhysicalBlock


class ReadingOrderResolver:
    """Stateless processor sorting document blocks into natural reading order."""

    @classmethod
    def resolve(cls, layout: DocumentLayout) -> Sequence[PhysicalBlock]:
        """Resolve and sort layout blocks sequentially.

        Args:
            layout: The physical document layout containing blocks.

        Returns:
            A list of sorted PhysicalBlock references in natural reading order.
        """
        blocks = list(layout.blocks)
        
        # Sort key: Page number of the first line, then global line number of the first line
        def get_sort_key(block: PhysicalBlock) -> tuple[int, int]:
            if not block.lines:
                return (9999, 9999)  # Fallback for empty blocks
            first_line = block.lines[0]
            return (first_line.page_number, first_line.line_number)

        blocks.sort(key=get_sort_key)
        return blocks
