"""Dedicated exception classes for Project Extraction.

Purpose:
    Define domain-specific errors for project candidate detection,
    validation, normalization, assembly, and building.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class ProjectExtractionError(EntityExtractionError):
    """Base exception for all project extraction failures."""


class ProjectCandidateValidationError(ProjectExtractionError):
    """Raised when a project candidate fails minimum structure validation."""


class ProjectNormalizationError(ProjectExtractionError):
    """Raised when normalizing raw project fields fails."""


class ProjectAssemblyError(ProjectExtractionError):
    """Raised when grouping evidence into compound project records fails."""


class ProjectBuilderError(ProjectExtractionError):
    """Raised when compiling project entities into domain models fails."""
