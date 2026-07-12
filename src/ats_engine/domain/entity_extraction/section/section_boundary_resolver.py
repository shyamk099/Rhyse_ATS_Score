"""Section boundary resolver.

Purpose:
    Determine sequential segment ranges for each detected section.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.entity_extraction.section.exceptions import BoundaryResolutionError
from ats_engine.domain.entity_extraction.section.section_models import SectionCandidate


class SectionBoundary:
    """Intermediate boundary holder tracking segment index ranges for sections."""

    def __init__(
        self,
        section_type: str,
        start_idx: int,
        end_idx: int,
        candidate: SectionCandidate | None = None,
    ) -> None:
        self.section_type = section_type
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.candidate = candidate


class SectionBoundaryResolver:
    """Stateless processor compiling segment ranges for section groups in document order."""

    @classmethod
    def resolve_boundaries(
        cls,
        document: CanonicalDocument,
        validated_candidates: Sequence[SectionCandidate],
    ) -> Sequence[SectionBoundary]:
        """Group segments into sequential section boundaries based on valid headings.

        Args:
            document: The CanonicalDocument to process.
            validated_candidates: Validated SectionCandidates.

        Returns:
            A sequence of SectionBoundaries.

        Raises:
            BoundaryResolutionError: If boundary mapping sequence audits fail.
        """
        layout = document.document_layout
        segments = document.segment_collection.segments

        if not segments:
            return []

        # 1. Map physical block key to block index
        def block_key(b) -> str:
            if not b.lines:
                return "empty"
            first_line = b.lines[0]
            return f"{first_line.page_number}_{first_line.line_number}"

        block_key_to_idx = {block_key(b): idx for idx, b in enumerate(layout.blocks)}

        # 2. Map segment index -> validated candidate if the segment starts with a candidate heading block
        segment_headings: dict[int, SectionCandidate] = {}
        candidate_map = {c.block_index: c for c in validated_candidates}

        for seg_idx, segment in enumerate(segments):
            if not segment.associated_blocks:
                continue
            first_block = segment.associated_blocks[0]
            first_block_idx = block_key_to_idx.get(block_key(first_block))
            if first_block_idx in candidate_map:
                segment_headings[seg_idx] = candidate_map[first_block_idx]

        # 3. Compile boundaries sequentially in original segment order
        boundaries: list[SectionBoundary] = []
        total_segments = len(segments)
        
        # Check if there is text before the first section heading
        first_heading_seg_idx = min(segment_headings.keys()) if segment_headings else total_segments
        if first_heading_seg_idx > 0:
            boundaries.append(
                SectionBoundary(
                    section_type="UNKNOWN",
                    start_idx=0,
                    end_idx=first_heading_seg_idx - 1,
                    candidate=None,
                )
            )

        # Iterate segment transitions to create boundary objects
        sorted_heading_indices = sorted(segment_headings.keys())
        for i, curr_idx in enumerate(sorted_heading_indices):
            candidate = segment_headings[curr_idx]
            
            # End index is either the segment before the next heading, or the final segment
            if i + 1 < len(sorted_heading_indices):
                next_idx = sorted_heading_indices[i + 1]
                end_idx = next_idx - 1
            else:
                end_idx = total_segments - 1

            boundaries.append(
                SectionBoundary(
                    section_type=candidate.section_type,
                    start_idx=curr_idx,
                    end_idx=end_idx,
                    candidate=candidate,
                )
            )

        return boundaries
