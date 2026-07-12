"""Unit tests for the Experience Extraction engine.

Purpose:
    Verify compound entity assembly, raw date preservation, company/title detection,
    current employment flags, structured responsibility lists, canonical IDs,
    and deterministic confidence reasoning.
"""

from __future__ import annotations

import unittest

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
from ats_engine.domain.entity_extraction.section.section_models import (
    Section,
    SectionCollection,
    SectionDetectionStatistics,
    SectionMetadata,
)
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules
from ats_engine.domain.entity_extraction.experience.service import ExperienceExtractionService


class ExperienceExtractionTests(unittest.TestCase):
    """Test suite validating compound experience entity extraction."""

    def setUp(self) -> None:
        """Initialize the experience extraction service."""
        self._service = ExperienceExtractionService()

    def test_extracts_single_experience_with_company_and_title(self) -> None:
        """Pipeline extracts a compound experience with company, title, and dates."""
        text = "Senior Developer at Acme Corp\nJanuary 2020 - December 2023\n- Built REST APIs\n- Deployed microservices"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        self.assertIsInstance(collection, ExperienceCollection)
        self.assertEqual(1, collection.statistics.total_experiences)

        exp = collection.entities[0]
        self.assertTrue(exp.experience_id.startswith("EXP-"))
        self.assertIsNotNone(exp.job_title)
        self.assertIn("Developer", exp.job_title)
        self.assertIsNotNone(exp.company_name)
        self.assertIn("Acme Corp", exp.company_name)
        self.assertEqual("January 2020", exp.start_date_raw)
        self.assertEqual("December 2023", exp.end_date_raw)
        self.assertFalse(exp.is_current)
        self.assertEqual(2, len(exp.responsibilities))
        self.assertIn("Built REST APIs", exp.responsibilities)

    def test_detects_current_employment(self) -> None:
        """Pipeline detects current employment when 'present' indicator is used."""
        text = "Software Engineer at Tech Solutions\nMarch 2022 - Present\n- Developing features"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        self.assertEqual(1, collection.statistics.total_experiences)
        self.assertEqual(1, collection.statistics.current_employment_count)

        exp = collection.entities[0]
        self.assertTrue(exp.is_current)
        self.assertEqual("March 2022", exp.start_date_raw)

    def test_handles_missing_dates_gracefully(self) -> None:
        """Pipeline extracts experience record even when dates are absent."""
        text = "Junior Analyst at Global Consulting\n- Performed data analysis"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        self.assertEqual(1, len(collection.entities))
        exp = collection.entities[0]
        self.assertIsNone(exp.start_date_raw)
        self.assertIsNone(exp.end_date_raw)
        self.assertIsNotNone(exp.job_title)

    def test_handles_missing_company_gracefully(self) -> None:
        """Pipeline extracts experience when company name is undetected."""
        text = "Lead Developer\nJune 2019 - August 2021\n- Led team of 5"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        self.assertEqual(1, len(collection.entities))
        exp = collection.entities[0]
        self.assertIsNone(exp.company_name)
        self.assertIn("Developer", exp.job_title)

    def test_extracts_multiple_experiences(self) -> None:
        """Pipeline extracts multiple independent experience records."""
        doc, sections = self._create_document_and_sections([
            ("EXPERIENCE", "Senior Engineer at Alpha Technologies\nJan 2020 - Present\n- Built systems"),
            ("EXPERIENCE", "Junior Developer at Beta Corp\nMay 2018 - Dec 2019\n- Wrote tests"),
        ])

        collection = self._service.extract_experience(doc, sections)

        self.assertEqual(2, collection.statistics.total_experiences)
        self.assertEqual("EXP-00000001", collection.entities[0].experience_id)
        self.assertEqual("EXP-00000002", collection.entities[1].experience_id)

    def test_detects_employment_type(self) -> None:
        """Pipeline detects employment type from configurable mappings."""
        text = "Contract Developer at Data Systems\nJan 2021 - Jun 2021"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertEqual("Contract", collection.entities[0].employment_type)

    def test_responsibilities_preserve_ordering(self) -> None:
        """Responsibilities maintain document order as a structured tuple."""
        text = "Software Architect at Cloud Corp\nJan 2020 - Dec 2022\n- Designed systems\n- Reviewed code\n- Mentored juniors"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        exp = collection.entities[0]
        self.assertEqual(3, len(exp.responsibilities))
        self.assertEqual("Designed systems", exp.responsibilities[0])
        self.assertEqual("Reviewed code", exp.responsibilities[1])
        self.assertEqual("Mentored juniors", exp.responsibilities[2])

    def test_confidence_includes_explainability(self) -> None:
        """Every experience entity has deterministic confidence and a human-readable reason."""
        text = "Senior Developer at Acme Corp\nJanuary 2020 - December 2023"
        doc, sections = self._create_document_and_sections(
            [("EXPERIENCE", text)]
        )

        collection = self._service.extract_experience(doc, sections)

        exp = collection.entities[0]
        self.assertGreater(exp.confidence, 0.0)
        self.assertLessEqual(exp.confidence, 1.0)
        self.assertIn("Matched rules:", exp.confidence_reason)
        self.assertTrue(len(exp.matched_rules) > 0)

    def test_respects_extraction_scope(self) -> None:
        """Pipeline only extracts from sections matching configured scope."""
        doc, sections = self._create_document_and_sections([
            ("SKILLS", "Senior Developer at Phantom Corp\nJan 2020 - Dec 2023"),
            ("EXPERIENCE", "Junior Analyst at Real Corp\nFeb 2018 - Jan 2020"),
        ])

        collection = self._service.extract_experience(doc, sections)

        # Default scope is EXPERIENCE only
        self.assertEqual(1, len(collection.entities))
        self.assertIn("Real Corp", collection.entities[0].company_name)

    def _create_document_and_sections(
        self, section_texts: list[tuple[str, str]]
    ) -> tuple[CanonicalDocument, SectionCollection]:
        blocks = []
        segments_list = []
        sections_list = []
        full_text_list = []
        block_idx = 1

        for stype, text in section_texts:
            full_text_list.append(text)
            line = PhysicalLine(
                text=text,
                line_number=block_idx,
                page_number=1,
                indentation_spaces=0,
                character_count=len(text),
            )
            block = PhysicalBlock(
                block_type=LayoutBlockType.TEXT,
                lines=(line,),
                raw_text=text,
            )
            blocks.append(block)
            metadata = SegmentMetadata(
                segment_id=f"segment_{block_idx:04d}",
                reading_order=block_idx,
                page_range=(1, 1),
                block_range=(block_idx, block_idx),
                character_count=len(text),
                line_count=1,
            )
            segment = DocumentSegment(
                segment_id=f"segment_{block_idx:04d}",
                text_content=text,
                metadata=metadata,
                associated_blocks=(block,),
            )
            segments_list.append(segment)
            sec_meta = SectionMetadata(
                section_type=stype,
                page_range=(1, 1),
                start_line=block_idx,
                end_line=block_idx,
                confidence=1.0,
                confidence_reason="Mock testing section setup",
            )
            section = Section(
                section_type=stype,
                text_content=text,
                metadata=sec_meta,
                associated_segments=(segment,),
            )
            sections_list.append(section)
            block_idx += 1

        full_text = "\n\n".join(full_text_list)
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
        doc = CanonicalDocument(
            canonical_id="doc_123456",
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            metadata=meta,
            statistics=stats,
        )

        sec_stats = SectionDetectionStatistics(
            section_counts={s: 1 for s, _ in section_texts},
            total_sections=len(sections_list),
            execution_duration_seconds=0.01,
        )
        sec_collection = SectionCollection(
            sections=tuple(sections_list),
            statistics=sec_stats,
        )
        return doc, sec_collection
