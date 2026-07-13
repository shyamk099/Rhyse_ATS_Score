"""Canonical Entity Collection and Validation module.

Purpose:
    Expose services, rules, models, exception hierarchy, and pipeline
    components for Canonical Entity Collection and Validation.
"""

from ats_engine.domain.entity_extraction.canonical.exceptions import (
    CanonicalCollectionError,
    DuplicateResolutionError,
    EntityValidationError,
    CrossReferenceValidationError,
)
from ats_engine.domain.entity_extraction.canonical.canonical_models import (
    CanonicalEntityCollection,
    ValidationErrorDetail,
    ValidationSummary,
    EntityStatistics,
)
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.canonical.pipeline import CanonicalEntityCollectionPipeline
from ats_engine.domain.entity_extraction.canonical.service import CanonicalEntityCollectionService

__all__ = [
    "CanonicalCollectionError",
    "DuplicateResolutionError",
    "EntityValidationError",
    "CrossReferenceValidationError",
    "CanonicalEntityCollection",
    "ValidationErrorDetail",
    "ValidationSummary",
    "EntityStatistics",
    "CanonicalValidationRules",
    "CanonicalEntityCollectionPipeline",
    "CanonicalEntityCollectionService",
]
