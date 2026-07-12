"""Entity extraction foundation package.

Purpose:
    Expose generic abstract extractor interfaces, registries, pipelines,
    and models for structural entity parsing.
"""

from ats_engine.domain.entity_extraction.exceptions import (
    ContextValidationError,
    EntityExtractionError,
    ExtractorRegistrationError,
    PipelineExecutionError,
    UnknownExtractorError,
)
from ats_engine.domain.entity_extraction.extractor import EntityExtractor
from ats_engine.domain.entity_extraction.factory import EntityExtractorFactory
from ats_engine.domain.entity_extraction.models import (
    EntityCollection,
    EntityExtractionContext,
    EntityExtractionStatistics,
    EntityLocation,
    ExtractedEntity,
)
from ats_engine.domain.entity_extraction.pipeline import EntityExtractionPipeline
from ats_engine.domain.entity_extraction.registry import EntityExtractorRegistry
from ats_engine.domain.entity_extraction.service import EntityExtractionService

__all__ = [
    "ContextValidationError",
    "EntityExtractionError",
    "ExtractorRegistrationError",
    "PipelineExecutionError",
    "UnknownExtractorError",
    "EntityExtractor",
    "EntityExtractorFactory",
    "EntityCollection",
    "EntityExtractionContext",
    "EntityExtractionStatistics",
    "EntityLocation",
    "ExtractedEntity",
    "EntityExtractionPipeline",
    "EntityExtractorRegistry",
    "EntityExtractionService",
]
