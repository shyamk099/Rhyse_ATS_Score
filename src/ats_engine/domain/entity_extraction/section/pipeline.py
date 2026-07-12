"""Section detection pipeline.

Purpose:
    Coordinate candidate scanning, heading validation, boundary grouping,
    and statistics assembly.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.section.heading_validator import HeadingValidator
from ats_engine.domain.entity_extraction.section.section_boundary_resolver import SectionBoundaryResolver
from ats_engine.domain.entity_extraction.section.section_builder import SectionBuilder
from ats_engine.domain.entity_extraction.section.section_candidate_builder import SectionCandidateBuilder
from ats_engine.domain.entity_extraction.section.section_models import (
    SectionCollection,
    SectionDetectionStatistics,
)
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules


class SectionDetectionPipeline:
    """Stateless pipeline resolving boundaries and building SectionCollection."""

    @classmethod
    def execute(cls, document: CanonicalDocument, rules: SectionDetectionRules) -> SectionCollection:
        """Run candidate building, validation, grouping, and packaging.

        Args:
            document: Canonical document.
            rules: Configured extraction patterns.

        Returns:
            The compiled, immutable SectionCollection container.
        """
        start_time = time.perf_counter()

        # 1. Scans physical layout blocks to build candidates
        candidates = SectionCandidateBuilder.find_candidates(document, rules)

        # 2. Audits candidates against word length / format limits
        validated_candidates = [
            cand for cand in candidates if HeadingValidator.validate(cand, rules)
        ]

        # 3. Splits layout boundaries sequentially
        boundaries = SectionBoundaryResolver.resolve_boundaries(document, validated_candidates)

        # 4. Aggregates segment blocks into sections
        sections_list = []
        section_counts: dict[str, int] = {}
        segments = document.segment_collection.segments

        for boundary in boundaries:
            section = SectionBuilder.build_section(boundary, segments, rules)
            sections_list.append(section)

            stype = section.section_type
            section_counts[stype] = section_counts.get(stype, 0) + 1

        duration = time.perf_counter() - start_time

        statistics = SectionDetectionStatistics(
            section_counts=section_counts,
            total_sections=len(sections_list),
            execution_duration_seconds=duration,
        )

        return SectionCollection(
            sections=tuple(sections_list),
            statistics=statistics,
        )
