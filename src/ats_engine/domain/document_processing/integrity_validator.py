"""Document physical integrity validator.

Purpose:
    Perform standalone structure checking to catch empty documents, invalid page numbers,
    empty segments, and layout holes.
"""

from __future__ import annotations

from ats_engine.domain.document_processing.exceptions import IntegrityValidationError
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules


class DocumentIntegrityValidator:
    """Stateless processor auditing structural elements and boundary conditions."""

    @classmethod
    def validate(
        cls,
        layout: DocumentLayout,
        segments: SegmentCollection,
        rules: CanonicalValidationRules,
    ) -> None:
        """Audit the layout and segments structure for page and block sequence holes.

        Args:
            layout: The physical DocumentLayout.
            segments: The SegmentCollection.
            rules: The validation rules configuration.

        Raises:
            IntegrityValidationError: If structural checks fail.
        """
        # 1. Empty document validations
        if layout.total_blocks == 0 or not layout.blocks:
            raise IntegrityValidationError("Document layout contains zero blocks.")
        if layout.total_lines == 0:
            raise IntegrityValidationError("Document layout contains zero lines.")
        if not segments.segments:
            raise IntegrityValidationError("Document segments collection is empty.")

        # 2. Empty segment validations
        for segment in segments.segments:
            if not segment.text_content.strip():
                raise IntegrityValidationError(f"Empty text content in segment: '{segment.segment_id}'.")
            if not segment.associated_blocks:
                raise IntegrityValidationError(f"Segment contains zero associated blocks: '{segment.segment_id}'.")

        # 3. Page index boundaries and sequencing validation
        page_numbers = {line.page_number for block in layout.blocks for line in block.lines}
        if not page_numbers:
            raise IntegrityValidationError("No page references discovered in layout lines.")

        max_page = max(page_numbers)
        if max_page > rules.max_allowed_pages:
            raise IntegrityValidationError(
                f"Page count {max_page} exceeds configured limit {rules.max_allowed_pages}."
            )

        expected_pages = set(range(1, max_page + 1))
        missing_pages = expected_pages - page_numbers
        if missing_pages:
            raise IntegrityValidationError(f"Layout has gaps in its page sequence. Missing pages: {missing_pages}")
