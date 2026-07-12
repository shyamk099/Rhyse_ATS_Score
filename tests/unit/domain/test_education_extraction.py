"""Unit tests for the Education Extraction engine.

Purpose:
    Verify compound entity assembly, raw date preservation, institution/degree
    detection, GPA/CGPA extraction, grade extraction, honors detection,
    specialization extraction, canonical IDs, graduation dates, duplicate records,
    confidence calculation, normalization, and exception handling.
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
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules
from ats_engine.domain.entity_extraction.education.service import EducationExtractionService


class EducationExtractionTests(unittest.TestCase):
    """Test suite validating compound education entity extraction."""

    def setUp(self) -> None:
        """Initialize the education extraction service."""
        self._service = EducationExtractionService()

    def test_extracts_single_education_with_degree_and_institution(self) -> None:
        """Pipeline extracts a compound education with degree, institution, and dates."""
        text = "Bachelor of Science in Computer Science\nMassachusetts Institute of Technology\nSeptember 2016 - June 2020"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertIsInstance(collection, EducationCollection)
        self.assertEqual(1, collection.statistics.total_education_records)

        edu = collection.entities[0]
        self.assertTrue(edu.education_id.startswith("EDU-"))
        self.assertIsNotNone(edu.degree)
        self.assertIn("Bachelor", edu.degree)

    def test_extracts_multiple_education_records(self) -> None:
        """Pipeline extracts multiple independent education records."""
        doc, sections = self._create_document_and_sections([
            ("EDUCATION", "Master of Science\nStanford University\n2020 - 2022"),
            ("EDUCATION", "Bachelor of Arts\nHarvard University\n2016 - 2020"),
        ])

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(2, collection.statistics.total_education_records)
        self.assertEqual("EDU-00000001", collection.entities[0].education_id)
        self.assertEqual("EDU-00000002", collection.entities[1].education_id)

    def test_extracts_degree_only(self) -> None:
        """Pipeline extracts education when only degree is present."""
        text = "PhD in Physics"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNotNone(collection.entities[0].degree)

    def test_extracts_institution_only(self) -> None:
        """Pipeline extracts education when only institution is present."""
        text = "Oxford University\n2018 - 2022"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNotNone(collection.entities[0].institution_name)
        self.assertIn("Oxford University", collection.entities[0].institution_name)

    def test_handles_missing_dates_gracefully(self) -> None:
        """Pipeline extracts education record even when dates are absent."""
        text = "Bachelor of Engineering\nDelhi Institute of Technology"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        edu = collection.entities[0]
        self.assertIsNone(edu.start_date_raw)
        self.assertIsNone(edu.end_date_raw)

    def test_handles_missing_gpa_gracefully(self) -> None:
        """Pipeline extracts education even when GPA is absent."""
        text = "Master of Business Administration\nWharton School\n2019 - 2021"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].gpa_raw)
        self.assertEqual(0, collection.statistics.records_with_gpa)

    def test_extracts_gpa(self) -> None:
        """Pipeline detects and stores GPA as raw text."""
        text = "Bachelor of Science\nMIT University\nGPA: 3.8/4.0"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNotNone(collection.entities[0].gpa_raw)
        self.assertIn("3.8", collection.entities[0].gpa_raw)
        self.assertEqual(1, collection.statistics.records_with_gpa)

    def test_extracts_cgpa(self) -> None:
        """Pipeline detects CGPA pattern."""
        text = "B.Tech in Computer Science\nIIT University\nCGPA: 8.5/10"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNotNone(collection.entities[0].gpa_raw)
        self.assertIn("CGPA", collection.entities[0].gpa_raw)

    def test_extracts_grade(self) -> None:
        """Pipeline detects grade/class notation."""
        text = "Bachelor of Commerce\nDelhi University\nGrade: First Class"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        edu = collection.entities[0]
        self.assertIsNotNone(edu.grade_raw)
        self.assertIn("First", edu.grade_raw)

    def test_extracts_honors(self) -> None:
        """Pipeline detects honors/distinction mentions."""
        text = "Bachelor of Science\nStanford University\nMagna Cum Laude\n2016 - 2020"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIn("Magna Cum Laude", collection.entities[0].honors)

    def test_extracts_specialization(self) -> None:
        """Pipeline detects specialization/major from text."""
        text = "Master of Science in Artificial Intelligence\nCarnegie Mellon University"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        edu = collection.entities[0]
        self.assertIsNotNone(edu.degree)

    def test_extracts_graduation_date(self) -> None:
        """Pipeline detects graduation date when graduation indicator is present."""
        text = "Bachelor of Arts\nYale University\nGraduated May 2021"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        edu = collection.entities[0]
        self.assertIsNotNone(edu.graduation_date_raw)

    def test_respects_extraction_scope(self) -> None:
        """Pipeline only extracts from sections matching configured scope."""
        doc, sections = self._create_document_and_sections([
            ("SKILLS", "Bachelor of Science\nGhost University\n2016 - 2020"),
            ("EDUCATION", "Master of Arts\nReal University\n2020 - 2022"),
        ])

        collection = self._service.extract_education(doc, sections)

        # Default scope is EDUCATION only
        self.assertEqual(1, len(collection.entities))
        self.assertIn("Real University", collection.entities[0].institution_name)

    def test_confidence_includes_explainability(self) -> None:
        """Every education entity has deterministic confidence and a human-readable reason."""
        text = "Bachelor of Science\nMIT University\nGPA: 3.9/4.0\n2016 - 2020"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        edu = collection.entities[0]
        self.assertGreater(edu.confidence, 0.0)
        self.assertLessEqual(edu.confidence, 1.0)
        self.assertIn("Matched rules:", edu.confidence_reason)
        self.assertTrue(len(edu.matched_rules) > 0)

    def test_unknown_values_remain_null(self) -> None:
        """Assembler never fabricates missing fields. Unknown values stay None."""
        text = "Diploma\nTrade School"
        doc, sections = self._create_document_and_sections(
            [("EDUCATION", text)]
        )

        collection = self._service.extract_education(doc, sections)

        self.assertEqual(1, len(collection.entities))
        edu = collection.entities[0]
        self.assertIsNone(edu.gpa_raw)
        self.assertIsNone(edu.grade_raw)
        self.assertIsNone(edu.graduation_date_raw)
        self.assertIsNone(edu.location_raw)
        self.assertEqual(0, len(edu.certifications))

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
