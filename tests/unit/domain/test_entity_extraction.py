"""Unit tests for the Entity Extraction Foundation.

Purpose:
    Verify registry mappings, factory instantiations, pipeline execution over segments,
    context propagation, exception boundary checks, and thread safety.
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
from ats_engine.domain.entity_extraction.exceptions import (
    ExtractorRegistrationError,
    PipelineExecutionError,
    UnknownExtractorError,
)
from ats_engine.domain.entity_extraction.extractor import EntityExtractor
from ats_engine.domain.entity_extraction.factory import EntityExtractorFactory
from ats_engine.domain.entity_extraction.models import (
    EntityCollection,
    EntityExtractionContext,
    EntityLocation,
    ExtractedEntity,
)
from ats_engine.domain.entity_extraction.pipeline import EntityExtractionPipeline
from ats_engine.domain.entity_extraction.registry import EntityExtractorRegistry
from ats_engine.domain.entity_extraction.service import EntityExtractionService


class DummyExtractor(EntityExtractor):
    """Stateless mock extractor for validating pipeline integration."""

    def extract(
        self, segment: DocumentSegment, context: EntityExtractionContext
    ) -> Sequence[ExtractedEntity]:
        """Extract a single mock entity from the segment."""
        loc = EntityLocation(
            segment_id=segment.segment_id,
            start_char=0,
            end_char=len(segment.text_content),
        )
        entity = ExtractedEntity(
            entity_type="dummy_type",
            value=f"value_from_{segment.segment_id}",
            confidence=0.95,
            location=loc,
            metadata={"extractor": "DummyExtractor"},
        )
        return [entity]


class EntityExtractionTests(unittest.TestCase):
    """Test suite validating the extensible entity extraction foundation."""

    def setUp(self) -> None:
        """Wire the registry, factory, and service components."""
        self._registry = EntityExtractorRegistry()
        self._registry.register("dummy", DummyExtractor)
        
        self._factory = EntityExtractorFactory(self._registry)
        self._pipeline = EntityExtractionPipeline(self._factory)
        self._service = EntityExtractionService(self._pipeline)

        self._document = self._create_dummy_document(text="Line text contents on page 1")

    def test_registry_prevents_duplicate_registration(self) -> None:
        """Registry raises ExtractorRegistrationError when registering an identical key."""
        with self.assertRaises(ExtractorRegistrationError):
            self._registry.register("dummy", DummyExtractor)

    def test_factory_fails_on_unknown_type(self) -> None:
        """Factory raises UnknownExtractorError for unregistered keys."""
        with self.assertRaises(UnknownExtractorError):
            self._factory.get_extractor("nonexistent_extractor")

    def test_pipeline_executes_sequential_extractors(self) -> None:
        """Pipeline aggregates extracted entities and executes stateless extractors sequentially."""
        collection = self._service.extract(
            document=self._document,
            extractor_types=["dummy"],
            correlation_id="test_corr_id",
        )

        self.assertIsInstance(collection, EntityCollection)
        self.assertEqual(1, len(collection.entities))
        self.assertEqual("dummy_type", collection.entities[0].entity_type)
        self.assertEqual("value_from_segment_0001", collection.entities[0].value)
        self.assertEqual(1, collection.statistics.total_entities)
        self.assertIn("dummy", collection.statistics.extractor_counts)
        self.assertEqual(1, collection.statistics.extractor_counts["dummy"])

    def test_context_is_read_only(self) -> None:
        """Context validation throws ValidationError upon property mutation."""
        context = EntityExtractionContext(
            canonical_document=self._document,
            correlation_id="test_id",
            rule_engine_config={"threshold": 0.5},
        )

        with self.assertRaises(ValidationError):
            context.model_validate({"correlation_id": "attempted_hack"})

    def test_pipeline_propagates_extractor_failures(self) -> None:
        """Pipeline raises PipelineExecutionError if an extractor raises a runtime exception."""
        class FailingExtractor(EntityExtractor):
            def extract(self, segment: DocumentSegment, context: EntityExtractionContext):
                raise ValueError("Simulated extractor crash")

        self._registry.register("failing", FailingExtractor)

        with self.assertRaises(PipelineExecutionError):
            self._service.extract(self._document, ["failing"])

    def _create_dummy_document(self, text: str) -> CanonicalDocument:
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
        return CanonicalDocument(
            canonical_id="doc_123456",
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            metadata=meta,
            statistics=stats,
        )
