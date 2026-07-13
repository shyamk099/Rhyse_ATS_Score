"""Domain exception definitions for Feature Engineering.

Purpose:
    Define typed error hierarchies raised during registry operations,
    factory instantiation, or pipeline execution.
"""

from __future__ import annotations


class FeatureEngineeringError(Exception):
    """Base exception for all feature engineering faults."""


class RegistrationError(FeatureEngineeringError):
    """Raised when registry constraints are violated."""


class UnknownExtractorError(FeatureEngineeringError):
    """Raised when resolving an unregistered extractor class."""


class PipelineExecutionError(FeatureEngineeringError):
    """Raised when pipeline encounters a failure during extractor execution."""


class FeatureValidationError(FeatureEngineeringError):
    """Raised when an individual feature fails structural validation checks."""


class DuplicateFeatureError(FeatureEngineeringError):
    """Raised when duplicate features violate resolver policy constraints."""


class CrossFeatureValidationError(FeatureEngineeringError):
    """Raised when consistency or reference checks fail across feature categories."""


class CanonicalCollectionBuildError(FeatureEngineeringError):
    """Raised when canonical collection building fails due to structural or validation issues."""

