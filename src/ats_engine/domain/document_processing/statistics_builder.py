"""Document physical statistics builder.

Purpose:
    Compile aggregated physical counts (characters, lines, paragraphs, blocks, segments)
    into a CanonicalStatistics instance.
"""

from __future__ import annotations

from ats_engine.domain.document_processing.canonical_models import CanonicalStatistics
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection


class DocumentStatisticsBuilder:
    """Stateless processor aggregating structural metrics of layout and segments."""

    @classmethod
    def build(
        cls,
        normalized: NormalizedDocument,
        layout: DocumentLayout,
        segments: SegmentCollection,
    ) -> CanonicalStatistics:
        """Compile statistics from document components.

        Args:
            normalized: The NormalizedDocument.
            layout: The DocumentLayout.
            segments: The SegmentCollection.

        Returns:
            A populated CanonicalStatistics instance.
        """
        total_chars = len(normalized.cleaned_content)
        
        # Determine paragraph count based on double spacing breaks
        paragraphs = [p for p in normalized.cleaned_content.split("\n\n") if p.strip()]
        total_paragraphs = len(paragraphs)

        total_lines = layout.total_lines
        total_blocks = layout.total_blocks
        total_segments = segments.total_segments

        return CanonicalStatistics(
            total_characters=total_chars,
            total_lines=total_lines,
            total_paragraphs=total_paragraphs,
            total_segments=total_segments,
            total_blocks=total_blocks,
        )
