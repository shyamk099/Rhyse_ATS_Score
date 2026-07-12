"""Dedicated exception classes for Contact Information Extraction.

Purpose:
    Define domain-specific exceptions for contact parsing, candidate validation,
    normalization, and configuration errors.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class ContactExtractionError(EntityExtractionError):
    """Base exception for all contact extraction failures."""


class CandidateValidationError(ContactExtractionError):
    """Raised when an extracted candidate fails sanity or structure checks."""


class NormalizationError(ContactExtractionError):
    """Raised when normalizing an extracted contact value fails."""


class PatternConfigurationError(ContactExtractionError):
    """Raised when regex compile patterns from the Rule Engine are invalid."""
