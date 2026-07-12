"""Dedicated exception hierarchy for the Entity Extraction domain.

Purpose:
    Define strict, domain-specific error classes for extractor registration,
    factory lookups, pipeline execution, and validation failures.
"""

class EntityExtractionError(Exception):
    """Base exception for all entity extraction errors."""


class ExtractorRegistrationError(EntityExtractionError):
    """Raised when registering an extractor fails (e.g. duplicate types)."""


class UnknownExtractorError(EntityExtractionError):
    """Raised when looking up an extractor type that is not registered."""


class PipelineExecutionError(EntityExtractionError):
    """Raised when pipeline execution encounters a runtime exception."""


class ContextValidationError(EntityExtractionError):
    """Raised when the validation of the extraction context fails."""
