"""Unit tests for the logical Document Section Detection engine.

Purpose:
    Verify candidate block classification, synonym alias validation, sequential
    boundary resolution, independent repeated sections, and fallback UNKNOWN blocks.
"""

from __future__ import annotations

import unittest
from typing import Sequence
from pydantic import ValidationError

from ats_engine.domain.document_processing.canonical_models import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalStatistics,
)
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import (
    BlockType as LayoutBlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.segmentation_models import (
    DocumentSegment,
    SegmentCollection,
    SegmentMetadata,
)
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules
from ats_engine.domain.entity_extraction.section.service import SectionDetectionService


class SectionDetectionTests(unittest.TestCase):
    """Test suite validating heuristics-based segment section grouping."""

    def setUp(self) -> None:
        """Initialize the section detection service."""
        self._service = SectionDetectionService()

    def test_detects_single_section_and_fallback_unknown(self) -> None:
        """Service groups blocks before the first heading as UNKNOWN and starts the logical section at the heading."""
        # Line 1: unknown intro content, Line 2: heading alias, Line 3: section content
        lines = ["My Name\nAddress", "EXPERIENCE", "Job Title - Company"]
        blocks = [
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=1, text="My Name\nAddress"),
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=3, text="EXPERIENCE"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=4, text="Job Title - Company"),
        ]
        doc = self._create_document(blocks)

        collection = self._service.detect_sections(doc)

        self.assertEqual(2, collection.statistics.total_sections)
        
        # Section 1: UNKNOWN fallback (intro)
        sec_unknown = collection.sections[0]
        self.assertEqual("UNKNOWN", sec_unknown.section_type)
        self.assertEqual("My Name\nAddress", sec_unknown.text_content)

        # Section 2: EXPERIENCE logical block
        sec_exp = collection.sections[1]
        self.assertEqual("EXPERIENCE", sec_exp.section_type)
        self.assertIn("Job Title - Company", sec_exp.text_content)
        self.assertEqual(0.95, sec_exp.metadata.confidence)  # Alias match confidence

    def test_handles_repeated_sections_independently(self) -> None:
        """Boundary resolver maintains repeated section sequences independently in document order."""
        # Skills -> Experience -> Skills
        blocks = [
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=1, text="SKILLS"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=2, text="Python, Java"),
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=3, text="WORK HISTORY"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=4, text="Software Dev"),
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=5, text="SKILLS"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=6, text="SQL, Git"),
        ]
        doc = self._create_document(blocks)

        collection = self._service.detect_sections(doc)

        # Verify 3 sections are kept separate (no merging)
        self.assertEqual(3, collection.statistics.total_sections)
        self.assertEqual("SKILLS", collection.sections[0].section_type)
        self.assertEqual("EXPERIENCE", collection.sections[1].section_type)  # WORK HISTORY aliases to EXPERIENCE
        self.assertEqual("SKILLS", collection.sections[2].section_type)

        self.assertEqual("SKILLS\n\nPython, Java", collection.sections[0].text_content)
        self.assertEqual("SKILLS\n\nSQL, Git", collection.sections[2].text_content)

    def test_heuristic_capitalization_matches_unknown_type(self) -> None:
        """Physical headings not matching known aliases are classified as UNKNOWN sections with default confidence."""
        # "CUSTOM HEADING" is not a configured alias
        blocks = [
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=1, text="CUSTOM HEADING"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=2, text="Some text here"),
        ]
        doc = self._create_document(blocks)

        collection = self._service.detect_sections(doc)

        self.assertEqual(1, collection.statistics.total_sections)
        self.assertEqual("UNKNOWN", collection.sections[0].section_type)
        # Verify default heuristic confidence (0.7) and reason
        self.assertEqual(0.7, collection.sections[0].metadata.confidence)
        self.assertIn("Matched physical heading characteristics", collection.sections[0].metadata.confidence_reason)

    def test_respects_custom_rules_and_aliases(self) -> None:
        """Custom Rule Engine configurations override default aliases and confidence scores."""
        custom_rules = SectionDetectionRules(
            section_aliases={"CUSTOM_LOGICAL": ["custom header"]},
            heading_confidence_alias_match=0.99,
        )
        blocks = [
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=1, text="custom header"),
            self._create_block(LayoutBlockType.TEXT, page=1, start_line=2, text="Value details"),
        ]
        doc = self._create_document(blocks)

        collection = self._service.detect_sections(
            doc, 
            rule_engine_config={"section_detection_rules": custom_rules.model_dump()}
        )

        self.assertEqual(1, collection.statistics.total_sections)
        self.assertEqual("CUSTOM_LOGICAL", collection.sections[0].section_type)
        self.assertEqual(0.99, collection.sections[0].metadata.confidence)

    def test_section_models_are_immutable(self) -> None:
        """Section models are frozen preventing attribute mutation."""
        blocks = [
            self._create_block(LayoutBlockType.HEADING, page=1, start_line=1, text="SKILLS"),
        ]
        doc = self._create_document(blocks)
        collection = self._service.detect_sections(doc)

        with self.assertRaises(ValidationError):
            collection.sections[0].metadata.model_validate({"section_type": "HACKED"})

    def _create_block(self, block_type: LayoutBlockType, page: int, start_line: int, text: str = "text") -> PhysicalBlock:
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

    def _create_document(self, blocks: list[PhysicalBlock]) -> CanonicalDocument:
        full_text = "\n\n".join(b.raw_text for b in blocks)
        norm_doc = NormalizedDocument(
            cleaned_content=full_text,
            paragraph_count=len(blocks),
            line_count=len(blocks),
            char_count=len(full_text),
        )
        layout = DocumentLayout(
            blocks=tuple(blocks),
            total_blocks=len(blocks),
            total_lines=len(blocks),
        )
        
        # Create disjoint segments (1 segment per block to simplify test offset mappings)
        segments_list = []
        for idx, block in enumerate(blocks, start=1):
            metadata = SegmentMetadata(
                segment_id=f"segment_{idx:04d}",
                reading_order=idx,
                page_range=(1, 1),
                block_range=(idx, idx),
                character_count=len(block.raw_text),
                line_count=1,
            )
            segment = DocumentSegment(
                segment_id=f"segment_{idx:04d}",
                text_content=block.raw_text,
                metadata=metadata,
                associated_blocks=(block,),
            )
            segments_list.append(segment)

        segments = SegmentCollection(
            segments=tuple(segments_list),
            total_segments=len(segments_list),
            total_characters=len(full_text),
        )
        meta = CanonicalMetadata(
            canonical_id="doc_123456",
            source_filename="test.pdf",
            file_size_bytes=100,
            page_count=1,
            parser_used="PdfDocumentParser",
            encoding="utf-8",
        )
        stats = CanonicalStatistics(
            total_characters=len(full_text),
            total_lines=len(blocks),
            total_paragraphs=len(blocks),
            total_segments=len(segments_list),
            total_blocks=len(blocks),
        )
        return CanonicalDocument(
            canonical_id="doc_123456",
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            metadata=meta,
            statistics=stats,
        )
