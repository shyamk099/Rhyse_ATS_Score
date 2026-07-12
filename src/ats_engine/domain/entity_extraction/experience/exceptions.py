"""Dedicated exception classes for Experience Extraction.

Purpose:
    Define domain-specific errors for experience candidate detection,
    validation, normalization, assembly, and building.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class ExperienceExtractionError(EntityExtractionError):
    """Base exception for all experience extraction failures."""


class ExperienceCandidateValidationError(ExperienceExtractionError):
    """Raised when an experience candidate fails minimum structure validation."""


class ExperienceNormalizationError(ExperienceExtractionError):
    """Raised when normalizing raw experience fields fails."""


class ExperienceAssemblyError(ExperienceExtractionError):
    """Raised when grouping evidence into compound experience records fails."""


class ExperienceBuilderError(ExperienceExtractionError):
    """Raised when compiling experience entities into domain models fails."""
