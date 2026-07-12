"""Dedicated exception classes for Education Extraction.

Purpose:
    Define domain-specific errors for education candidate detection,
    validation, normalization, assembly, and building.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class EducationExtractionError(EntityExtractionError):
    """Base exception for all education extraction failures."""


class EducationCandidateValidationError(EducationExtractionError):
    """Raised when an education candidate fails minimum structure validation."""


class EducationNormalizationError(EducationExtractionError):
    """Raised when normalizing raw education fields fails."""


class EducationAssemblyError(EducationExtractionError):
    """Raised when grouping evidence into compound education records fails."""


class EducationBuilderError(EducationExtractionError):
    """Raised when compiling education entities into domain models fails."""
