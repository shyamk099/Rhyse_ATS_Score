"""Book 07 — Recommendation Engine Exceptions.

Purpose:
    Define typed exception hierarchy for the Resume Intelligence Engine.
    These exceptions are intentionally separate from Book 06's scoring exceptions
    to maintain clean architectural boundaries between Books.
"""

from __future__ import annotations


class RecommendationError(Exception):
    """Base exception for all recommendation engine failures."""


class RecommendationValidationError(RecommendationError):
    """Raised when input validation fails before recommendation generation."""


class RecommendationProviderError(RecommendationError):
    """Raised when a recommendation provider encounters an execution failure."""
