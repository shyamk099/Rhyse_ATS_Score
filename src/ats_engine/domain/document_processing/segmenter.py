"""Document segmenter orchestrator.

Purpose:
    Coordinate reading order sorting, segment compiling, and integrity validation.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.document_processing.reading_order import ReadingOrderResolver
from ats_engine.domain.document_processing.segment_builder import PhysicalSegmentBuilder
from ats_engine.domain.document_processing.segment_validator import SegmentValidator
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection
from ats_engine.domain.document_processing.segmentation_rules import SegmentationRules
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.infrastructure.logging.factory import LoggerFactory


class DocumentSegmenter:
    """Stateless orchestrator executing the full structural layout segmentation pipeline."""

    def __init__(self, rules: SegmentationRules, logger: logging.Logger | None = None) -> None:
        """Initialize the segmenter with rules and optional logger."""
        self._rules = rules
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def segment(self, layout: DocumentLayout) -> SegmentCollection:
        """Segment a physical DocumentLayout into an ordered collection of segments.

        Args:
            layout: The physical document layout containing blocks.

        Returns:
            A validated SegmentCollection instance.

        Raises:
            ValidationError: If any compiled segment schema is malformed.
            RuleValidationError: If segment validation checks fail.
        """
        self._logger.info("document_segmentation_started")

        # 1. Resolve reading order
        sorted_blocks = ReadingOrderResolver.resolve(layout)

        # 2. Build segments
        segments = PhysicalSegmentBuilder.build_segments(sorted_blocks, self._rules)

        # 3. Validate structural integrity
        SegmentValidator.validate(layout, segments)

        total_chars = sum(seg.metadata.character_count for seg in segments)

        self._logger.info(
            "document_segmentation_completed",
            extra={
                "total_segments": len(segments),
                "total_characters": total_chars,
            },
        )

        return SegmentCollection(
            segments=tuple(segments),
            total_segments=len(segments),
            total_characters=total_chars,
        )
