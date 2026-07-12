"""Document processing foundation package.

Purpose:
    Expose types, interfaces, services, and pipelines for raw document parsing, layout analysis,
    physical segmentation, and canonical validation.
"""

from ats_engine.domain.document_processing.docx_parser import DocxDocumentParser
from ats_engine.domain.document_processing.exceptions import (
    CorruptedDocumentError,
    DocumentProcessingError,
    DocumentReadError,
    NormalizationError,
    UnsupportedFormatError,
    SegmentValidationError,
    CanonicalDocumentValidationError,
    IntegrityValidationError,
    ConsistencyValidationError,
    StatisticsValidationError,
    AssemblyValidationError,
)
from ats_engine.domain.document_processing.factory import DocumentParserFactory
from ats_engine.domain.document_processing.models import (
    DocumentMetadata,
    NormalizedDocument,
    ParsingResult,
    RawDocument,
)
from ats_engine.domain.document_processing.normalization import TextNormalizer
from ats_engine.domain.document_processing.parser import DocumentParser
from ats_engine.domain.document_processing.pdf_parser import PdfDocumentParser
from ats_engine.domain.document_processing.registry import DocumentParserRegistry
from ats_engine.domain.document_processing.service import DocumentProcessingService
from ats_engine.domain.document_processing.structure_models import (
    BlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.structural_rules import StructuralAnalysisRules
from ats_engine.domain.document_processing.structural_analyzer import StructuralAnalyzer

# Milestone 2.3 exports
from ats_engine.domain.document_processing.segmentation_models import (
    DocumentSegment,
    SegmentCollection,
    SegmentMetadata,
)
from ats_engine.domain.document_processing.segmentation_rules import SegmentationRules
from ats_engine.domain.document_processing.reading_order import ReadingOrderResolver
from ats_engine.domain.document_processing.segment_builder import PhysicalSegmentBuilder
from ats_engine.domain.document_processing.segment_validator import SegmentValidator
from ats_engine.domain.document_processing.segmenter import DocumentSegmenter

# Milestone 2.4 exports
from ats_engine.domain.document_processing.canonical_models import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalStatistics,
)
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules
from ats_engine.domain.document_processing.canonical_builder import CanonicalDocumentBuilder
from ats_engine.domain.document_processing.canonical_assembler import CanonicalDocumentAssembler
from ats_engine.domain.document_processing.integrity_validator import DocumentIntegrityValidator
from ats_engine.domain.document_processing.consistency_validator import DocumentConsistencyValidator
from ats_engine.domain.document_processing.statistics_builder import DocumentStatisticsBuilder
from ats_engine.domain.document_processing.validation_service import DocumentValidationService

__all__ = [
    "DocxDocumentParser",
    "CorruptedDocumentError",
    "DocumentProcessingError",
    "DocumentReadError",
    "NormalizationError",
    "UnsupportedFormatError",
    "SegmentValidationError",
    "CanonicalDocumentValidationError",
    "IntegrityValidationError",
    "ConsistencyValidationError",
    "StatisticsValidationError",
    "AssemblyValidationError",
    "DocumentParserFactory",
    "DocumentMetadata",
    "NormalizedDocument",
    "ParsingResult",
    "RawDocument",
    "TextNormalizer",
    "DocumentParser",
    "PdfDocumentParser",
    "DocumentParserRegistry",
    "DocumentProcessingService",
    "BlockType",
    "DocumentLayout",
    "PhysicalBlock",
    "PhysicalLine",
    "StructuralAnalysisRules",
    "StructuralAnalyzer",
    "DocumentSegment",
    "SegmentCollection",
    "SegmentMetadata",
    "SegmentationRules",
    "ReadingOrderResolver",
    "PhysicalSegmentBuilder",
    "SegmentValidator",
    "DocumentSegmenter",
    "CanonicalDocument",
    "CanonicalMetadata",
    "CanonicalStatistics",
    "CanonicalValidationRules",
    "CanonicalDocumentBuilder",
    "CanonicalDocumentAssembler",
    "DocumentIntegrityValidator",
    "DocumentConsistencyValidator",
    "DocumentStatisticsBuilder",
    "DocumentValidationService",
]
