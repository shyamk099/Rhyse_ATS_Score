"""Unit tests for the Certification Extraction engine.

Purpose:
    Verify compound entity assembly, URL provenance preservation, skill ID
    resolution, credential ID/URL extraction, issue/expiry dates, missing values
    handling, duplicates, confidence calculations, normalization, and exception handling.
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
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules
from ats_engine.domain.entity_extraction.certification.service import CertificationExtractionService


class CertificationExtractionTests(unittest.TestCase):
    """Test suite validating compound certification entity extraction."""

    def setUp(self) -> None:
        """Initialize the certification extraction service."""
        self._service = CertificationExtractionService()

    def test_extracts_single_certification_with_name_and_issuer(self) -> None:
        """Pipeline extracts a compound certification with name, issuer, and dates."""
        text = "AWS Certified Solutions Architect\nissued by Amazon Web Services\nSeptember 2022 - September 2025"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertIsInstance(collection, CertificationCollection)
        self.assertEqual(1, collection.statistics.total_certifications)

        cert = collection.entities[0]
        self.assertTrue(cert.certification_id.startswith("CERT-"))
        self.assertEqual("AWS Certified Solutions Architect", cert.certification_name)
        self.assertEqual("Amazon Web Services", cert.issuing_organization)
        self.assertEqual("September 2022", cert.issue_date_raw)
        self.assertEqual("September 2025", cert.expiration_date_raw)

    def test_extracts_multiple_certifications(self) -> None:
        """Pipeline extracts multiple independent certification records."""
        doc, sections = self._create_document_and_sections([
            ("CERTIFICATIONS", "Project Management Professional\nissued by PMI\n2021"),
            ("CERTIFICATIONS", "Certified ScrumMaster\nissued by Scrum Alliance\n2022"),
        ])

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(2, collection.statistics.total_certifications)
        self.assertEqual("CERT-00000001", collection.entities[0].certification_id)
        self.assertEqual("CERT-00000002", collection.entities[1].certification_id)

    def test_credential_id_extraction(self) -> None:
        """Pipeline extracts credential ID using rule patterns."""
        text = "Certified ScrumMaster\nCredential ID: 12345-6789\nissued by Scrum Alliance"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertEqual("12345-6789", collection.entities[0].credential_id_raw)

    def test_credential_url_extraction(self) -> None:
        """Pipeline extracts credential URL with provenance preservation."""
        text = "AWS Architect\nVerify at https://credly.com/credentials/aws-solutions-architect"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        cert = collection.entities[0]
        self.assertIsNotNone(cert.credential_url)
        self.assertEqual("https://credly.com/credentials/aws-solutions-architect", cert.credential_url.original_value)
        self.assertEqual("configured_credential_url_pattern", cert.credential_url.matched_rule)

    def test_missing_organization_gracefully(self) -> None:
        """Pipeline extracts certification even if issuer/organization is missing."""
        text = "PMP Certification\nCredential ID: 987654"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].issuing_organization)

    def test_missing_dates_gracefully(self) -> None:
        """Pipeline extracts certification without dates."""
        text = "Certified ScrumMaster\nissued by Scrum Alliance"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].issue_date_raw)

    def test_missing_credential_id_gracefully(self) -> None:
        """Pipeline extracts certification without credential ID."""
        text = "PMP Certification\nissued by PMI\n2022"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].credential_id_raw)

    def test_skill_mapping_resolution(self) -> None:
        """Skills resolved to canonical Skill IDs if mappings exist, otherwise preserved as raw."""
        text = "AWS Certified Solutions Architect\n- Skill: AWS Cloud\n- Tech: in Docker"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        rules = {
            "certification_extraction_rules": {
                "skill_mappings": {
                    "aws cloud": "SKL-00000099",
                }
            }
        }

        collection = self._service.extract_certification(doc, sections, rule_engine_config=rules)

        self.assertEqual(1, len(collection.entities))
        cert = collection.entities[0]

        # Verify AWS Cloud resolved to Skill ID
        self.assertIn("SKL-00000099", cert.associated_skill_ids)

        # Verify Docker preserved raw
        self.assertIn("Docker", cert.associated_skills_raw)

    def test_confidence_calculation(self) -> None:
        """Every certification entity contains a scaled confidence score and reasons."""
        text = "AWS Certified Developer\nissued by Amazon Web Services\nCredential ID: 9911-22"
        doc, sections = self._create_document_and_sections(
            [("CERTIFICATIONS", text)]
        )

        collection = self._service.extract_certification(doc, sections)

        self.assertEqual(1, len(collection.entities))
        cert = collection.entities[0]
        self.assertTrue(cert.confidence > 0.0)
        self.assertIn("Matched rules:", cert.confidence_reason)

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
