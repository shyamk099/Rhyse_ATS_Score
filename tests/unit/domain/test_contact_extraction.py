"""Unit tests for Contact Information Extraction.

Purpose:
    Verify regex candidate detection, validation rules, normalizations,
    overlap resolution, and deterministic confidence values.
"""

from __future__ import annotations

import unittest
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalStatistics,
)
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import (
    BlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.segmentation_models import (
    DocumentSegment,
    SegmentCollection,
    SegmentMetadata,
)
from ats_engine.domain.entity_extraction.contact.contact_rules import ContactExtractionRules
from ats_engine.domain.entity_extraction.contact.extractor import ContactInformationExtractor
from ats_engine.domain.entity_extraction.models import EntityExtractionContext, ExtractedEntity


class ContactExtractionTests(unittest.TestCase):
    """Test suite validating pattern-based contact extraction."""

    def setUp(self) -> None:
        """Initialize extractor stateless reference."""
        self._extractor = ContactInformationExtractor()

    def test_extracts_valid_email_and_phone(self) -> None:
        """Extractor parses valid email formats and clean phone numbers."""
        text = "Contact me at shyam@example.com or call +1-415-555-0199."
        context = self._create_context(text)

        entities = self._extractor.extract(context.canonical_document.segment_collection.segments[0], context)

        # Expected: 1 email and 1 phone entity
        self.assertEqual(2, len(entities))
        
        email_entity = next(e for e in entities if e.entity_type == "email")
        phone_entity = next(e for e in entities if e.entity_type == "phone")

        self.assertEqual("shyam@example.com", email_entity.value)
        self.assertEqual(1.0, email_entity.confidence)
        
        self.assertEqual("+14155550199", phone_entity.value)
        self.assertEqual(0.9, phone_entity.confidence)

    def test_extracts_social_links_without_overlap(self) -> None:
        """Extractor parses LinkedIn/GitHub URLs and ensures portfolio does not double match them."""
        text = "Profiles: linkedin.com/in/shyamk and github.com/shyamk099 or myblog.com"
        context = self._create_context(text)

        entities = self._extractor.extract(context.canonical_document.segment_collection.segments[0], context)

        # Expected: 1 linkedin, 1 github, 1 portfolio (no double portfolio match on linkedin/github)
        self.assertEqual(3, len(entities))

        linkedin = next(e for e in entities if e.entity_type == "linkedin")
        github = next(e for e in entities if e.entity_type == "github")
        portfolio = next(e for e in entities if e.entity_type == "portfolio")

        self.assertEqual("linkedin.com/in/shyamk", linkedin.value)
        self.assertEqual("github.com/shyamk099", github.value)
        self.assertEqual("myblog.com", portfolio.value)

    def test_ignores_invalid_email_and_phone(self) -> None:
        """Extractor skips malformed email layouts and short/long phone strings."""
        # 'shyam@com' is invalid (no dot), '12345' is too short for phone
        text = "Invalid details: shyam@com or 12345"
        context = self._create_context(text)

        entities = self._extractor.extract(context.canonical_document.segment_collection.segments[0], context)
        self.assertEqual(0, len(entities))

    def test_normalizes_lower_case_and_trailing_slashes(self) -> None:
        """ContactNormalizer standardizes emails to lowercase and strips trailing slashes on links."""
        text = "Email: SHYAM@EXAMPLE.COM link: https://myblog.com/"
        context = self._create_context(text)

        entities = self._extractor.extract(context.canonical_document.segment_collection.segments[0], context)

        self.assertEqual(2, len(entities))
        email = next(e for e in entities if e.entity_type == "email")
        portfolio = next(e for e in entities if e.entity_type == "portfolio")

        self.assertEqual("shyam@example.com", email.value)
        self.assertEqual("https://myblog.com", portfolio.value)

    def test_respects_custom_regex_and_confidence_configs(self) -> None:
        """Custom Rule Engine configurations adjust patterns and weights dynamically."""
        # Configure a custom ruleset where github confidence is lowered to 0.4
        custom_rules = ContactExtractionRules(
            github_confidence=0.4,
        )
        text = "Profile: github.com/shyam"
        context = self._create_context(
            text, 
            config={"contact_extraction_rules": custom_rules.model_dump()}
        )

        entities = self._extractor.extract(context.canonical_document.segment_collection.segments[0], context)

        self.assertEqual(1, len(entities))
        self.assertEqual("github", entities[0].entity_type)
        self.assertEqual(0.4, entities[0].confidence)

    def _create_context(self, text: str, config: dict | None = None) -> EntityExtractionContext:
        norm_doc = NormalizedDocument(
            cleaned_content=text,
            paragraph_count=1,
            line_count=1,
            char_count=len(text),
        )
        line = PhysicalLine(
            text=text,
            line_number=1,
            page_number=1,
            indentation_spaces=0,
            character_count=len(text),
        )
        block = PhysicalBlock(
            block_type=BlockType.TEXT,
            lines=(line,),
            raw_text=text,
        )
        layout = DocumentLayout(
            blocks=(block,),
            total_blocks=1,
            total_lines=1,
        )
        metadata = SegmentMetadata(
            segment_id="segment_0001",
            reading_order=1,
            page_range=(1, 1),
            block_range=(1, 1),
            character_count=len(text),
            line_count=1,
        )
        segment = DocumentSegment(
            segment_id="segment_0001",
            text_content=text,
            metadata=metadata,
            associated_blocks=(block,),
        )
        segments = SegmentCollection(
            segments=(segment,),
            total_segments=1,
            total_characters=len(text),
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
            total_characters=len(text),
            total_lines=1,
            total_paragraphs=1,
            total_segments=1,
            total_blocks=1,
        )
        doc = CanonicalDocument(
            canonical_id="doc_123456",
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            metadata=meta,
            statistics=stats,
        )
        return EntityExtractionContext(
            canonical_document=doc,
            correlation_id="test_corr",
            rule_engine_config=config or {},
        )
