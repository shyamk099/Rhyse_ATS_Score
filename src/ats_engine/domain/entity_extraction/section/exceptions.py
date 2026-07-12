"""Dedicated exception classes for Document Section Detection.

Purpose:
    Define domain-specific exceptions for section scanning, validation,
    boundary resolution, and builder errors.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class SectionDetectionError(EntityExtractionError):
    """Base exception for all section detection failures."""


class HeadingValidationError(SectionDetectionError):
    """Raised when a heading candidate fails validation checks."""


class BoundaryResolutionError(SectionDetectionError):
    """Raised when boundary mapping sequence audits fail."""


class SectionBuilderError(SectionDetectionError):
    """Raised when compiling segment collections into Section models fails."""
