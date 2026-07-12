"""Section model builder.

Purpose:
    Compile resolved boundaries and segment groups into immutable Section models.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.entity_extraction.section.section_boundary_resolver import SectionBoundary
from ats_engine.domain.entity_extraction.section.section_models import Section, SectionMetadata
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules


class SectionBuilder:
    """Stateless builder aggregating segment ranges, line/page boundaries, and stats into Sections."""

    @classmethod
    def build_section(
        cls,
        boundary: SectionBoundary,
        segments: Sequence[DocumentSegment],
        rules: SectionDetectionRules,
    ) -> Section:
        """Create a Section container for the boundary range.

        Args:
            boundary: The resolved boundary.
            segments: The absolute DocumentSegment collection.
            rules: The rules parameter mapping thresholds.

        Returns:
            The immutable Section container.
        """
        section_segments = segments[boundary.start_idx : boundary.end_idx + 1]

        # Aggregate text contents
        text_content = "\n\n".join(seg.text_content for seg in section_segments)

        # Collect page indexes and line boundaries
        pages: list[int] = []
        lines: list[int] = []
        for seg in section_segments:
            pages.extend(seg.metadata.page_range)
            lines.extend(seg.metadata.block_range)

        page_range = (min(pages), max(pages)) if pages else (1, 1)
        start_line = min(lines) if lines else 1
        end_line = max(lines) if lines else 1

        # Resolve confidence settings and explanation notes
        if boundary.candidate:
            confidence = boundary.candidate.confidence
            reason = boundary.candidate.confidence_reason
        else:
            confidence = 1.0  # Fallback UNKNOWN section blocks are physically exact
            reason = "Physical fallback block collection preceding first heading"

        metadata = SectionMetadata(
            section_type=boundary.section_type,
            page_range=page_range,
            start_line=start_line,
            end_line=end_line,
            confidence=confidence,
            confidence_reason=reason,
        )

        return Section(
            section_type=boundary.section_type,
            text_content=text_content,
            metadata=metadata,
            associated_segments=tuple(section_segments),
        )
