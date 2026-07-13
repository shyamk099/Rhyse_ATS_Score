"""Dedicated exception classes for Canonical Entity Collection and Validation.

Purpose:
    Define domain-specific errors for collection building, structural validation,
    duplicate resolution, and cross-reference checks.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class CanonicalCollectionError(EntityExtractionError):
    """Base exception for all canonical collection failures."""


class EntityValidationError(CanonicalCollectionError):
    """Raised when structural validation of an entity fails."""


class CrossReferenceValidationError(CanonicalCollectionError):
    """Raised when cross-reference checks find broken entity associations."""


class DuplicateResolutionError(CanonicalCollectionError):
    """Raised when duplicate entities cannot be resolved under the configured policies."""
