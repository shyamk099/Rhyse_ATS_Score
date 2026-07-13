"""Dedicated exception classes for Certification Extraction.

Purpose:
    Define domain-specific errors for certification candidate detection,
    validation, normalization, assembly, and building.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class CertificationExtractionError(EntityExtractionError):
    """Base exception for all certification extraction failures."""


class CertificationCandidateValidationError(CertificationExtractionError):
    """Raised when a certification candidate fails minimum structure validation."""


class CertificationNormalizationError(CertificationExtractionError):
    """Raised when normalizing raw certification fields fails."""


class CertificationAssemblyError(CertificationExtractionError):
    """Raised when grouping evidence into compound certification records fails."""


class CertificationBuilderError(CertificationExtractionError):
    """Raised when compiling certification entities into domain models fails."""
