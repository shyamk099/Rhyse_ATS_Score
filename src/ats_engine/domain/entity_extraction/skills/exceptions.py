"""Dedicated exception classes for Skill Extraction.

Purpose:
    Define domain-specific errors for candidate validation, normalizations,
    matcher configurations, and pipeline failures.
"""

from ats_engine.domain.entity_extraction.exceptions import EntityExtractionError


class SkillExtractionError(EntityExtractionError):
    """Base exception for all skill extraction failures."""


class SkillCandidateValidationError(SkillExtractionError):
    """Raised when a candidate skill fails structure or length validation."""


class SkillNormalizationError(SkillExtractionError):
    """Raised when mapping matched skills to canonical representations fails."""


class SkillBuilderError(SkillExtractionError):
    """Raised when compiling skill entities into Domain ExtractedEntities fails."""


class MatcherConfigurationError(SkillExtractionError):
    """Raised when the matcher fails to configure or parse rule expressions."""
