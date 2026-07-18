"""Domain exception definitions for ATS Matching Engine.

Purpose:
    Define typed error hierarchies raised during registry operations,
    factory instantiation, or pipeline execution.
"""

from __future__ import annotations


class MatchingError(Exception):
    """Base exception for all matching faults."""


class UnknownMatcherError(MatchingError):
    """Raised when resolving an unregistered FeatureMatcher class."""


class MatcherRegistrationError(MatchingError):
    """Raised when registry constraints are violated."""


class PipelineExecutionError(MatchingError):
    """Raised when matching pipeline execution fails."""


class ContextValidationError(MatchingError):
    """Raised when context attributes fail validation."""


# New canonical match collection exceptions

class MatchValidationError(MatchingError):
    """Raised when one or more MatchResult entries fail structural validation."""


class DuplicateMatchError(MatchingError):
    """Raised when duplicate MatchResult entries are detected and cannot be resolved per policy."""


class CrossMatchValidationError(MatchingError):
    """Raised when cross‑collection invariants are violated (e.g., duplicate IDs across collections)."""


class CanonicalMatchCollectionBuildError(MatchingError):
    """Raised when building the final CanonicalMatchCollection fails for any reason."""
