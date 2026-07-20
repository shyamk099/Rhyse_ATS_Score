"""Exceptions for the ATS Scoring Engine.

Purpose:
    Define typed hierarchy of scoring validation, registration, and pipeline execution faults.
"""

from __future__ import annotations


class ScoringError(Exception):
    """Base exception for all scoring domain errors."""


class ScoringValidationError(ScoringError):
    """Raised when CanonicalMatchCollection or rules validation fails."""


class SkillScoringError(ScoringError):
    """Base exception for all skill scoring domain errors."""


class SkillValidationError(ScoringValidationError, SkillScoringError):
    """Raised when skill scoring validation checks fail."""


class ExperienceScoringError(ScoringError):
    """Base exception for all experience scoring domain errors."""


class ExperienceValidationError(ScoringValidationError, ExperienceScoringError):
    """Raised when experience scoring validation checks fail."""


class EducationScoringError(ScoringError):
    """Base exception for all education scoring domain errors."""


class EducationValidationError(ScoringValidationError, EducationScoringError):
    """Raised when education scoring validation checks fail."""


class ProjectScoringError(ScoringError):
    """Base exception for all project scoring domain errors."""


class ProjectValidationError(ScoringValidationError, ProjectScoringError):
    """Raised when project scoring validation checks fail."""


class CertificationScoringError(ScoringError):
    """Base exception for all certification scoring domain errors."""


class CertificationValidationError(ScoringValidationError, CertificationScoringError):
    """Raised when certification scoring validation checks fail."""







class ScoringPipelineError(ScoringError):
    """Raised when E2E scoring pipeline execution fails."""


class ScorerRegistrationError(ScoringError):
    """Raised when duplicate or invalid scorer classes are registered."""


class UnsupportedScorerError(ScoringError):
    """Raised when resolving an unsupported or unregistered scorer."""


class ScoreBuildError(ScoringError):
    """Raised when building statistics, metadata, or final score results fails."""


class OrchestrationError(ScoringError):
    """Base exception for all orchestration coordination failures."""


class ExecutionPlanError(OrchestrationError):
    """Raised when ExecutionPlan construction fails (duplicate priorities, empty registry, etc.)."""


class RegistryValidationError(OrchestrationError):
    """Raised when pre-flight registry validation detects structural or type violations."""


class AggregationError(ScoringError):
    """Base exception for all aggregation failures."""


class NormalizationError(AggregationError):
    """Raised when score normalization fails (e.g., maximum_score is zero or None)."""


class WeightConfigurationError(AggregationError):
    """Raised when weight configuration is invalid (e.g., weights do not sum to 1.0)."""


class AggregationValidationError(AggregationError):
    """Raised when a ScoreResult fails pre-aggregation structural validation."""


class ExplainabilityError(ScoringError):
    """Base exception for all score explainability failures."""


class FormattingError(ExplainabilityError):
    """Raised when formatting explanation strings fails."""


class ExplainabilityValidationError(ExplainabilityError):
    """Raised when ScoreResult inputs fail validation checks before explainability processing."""
