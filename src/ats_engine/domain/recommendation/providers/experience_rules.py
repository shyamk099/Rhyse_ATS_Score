"""ExperienceRecommendationRules definition.

Purpose:
    Define deterministic rules governing experience recommendation categories.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ats_engine.domain.matching.models import MatchResult


class RecommendationAction(str, Enum):
    """Actions representing the decision outcome of experience evaluation."""

    NO_ACTION = "NO_ACTION"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    DURATION_GAP = "DURATION_GAP"


class ExperienceRecommendationRules:
    """Deterministic rules evaluating experience elements into recommendation actions."""

    def evaluate_missing(self, name: str) -> RecommendationAction:
        """Determine action for a missing experience requirement.

        Args:
            name: The experience requirement name.

        Returns:
            MISSING recommendation action.
        """
        if not name or name.strip() == "":
            return RecommendationAction.NO_ACTION
        return RecommendationAction.MISSING

    def evaluate_match(self, match: MatchResult) -> RecommendationAction:
        """Determine action for a matched experience requirement.

        Args:
            match: The MatchResult object.

        Returns:
            The resolved RecommendationAction.
        """
        attrs = getattr(match.metadata, "custom_attributes", {}) or {}
        val = attrs.get("match_type") or attrs.get("classification") or ""
        val = val.upper()

        if val in ("PARTIAL_MATCH", "PARTIAL"):
            return RecommendationAction.PARTIAL

        if val in ("UNDERQUALIFIED", "UNDER") or attrs.get("duration_gap", False) or attrs.get("insufficient_duration", False):
            return RecommendationAction.DURATION_GAP

        return RecommendationAction.NO_ACTION
