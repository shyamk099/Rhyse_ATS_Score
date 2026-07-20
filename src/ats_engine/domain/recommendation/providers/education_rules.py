"""EducationRecommendationRules definition.

Purpose:
    Define deterministic rules evaluating education elements into recommendation actions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from ats_engine.domain.recommendation.providers.base import RecommendationAction

if TYPE_CHECKING:
    from ats_engine.domain.matching.models import MatchResult


class EducationRecommendationRules:
    """Deterministic rules evaluating education elements into recommendation actions."""

    def evaluate_missing(self, name: str) -> RecommendationAction:
        """Determine action for a missing education requirement.

        Args:
            name: The education requirement name (e.g. 'Bachelor').

        Returns:
            MISSING recommendation action.
        """
        if not name or name.strip() == "":
            return RecommendationAction.NO_ACTION
        return RecommendationAction.MISSING

    def evaluate_match(self, match: MatchResult) -> RecommendationAction:
        """Determine action for a matched education requirement.

        Args:
            match: The MatchResult object.

        Returns:
            The resolved RecommendationAction.
        """
        attrs = getattr(match.metadata, "custom_attributes", {}) or {}
        val = attrs.get("match_type") or attrs.get("classification") or ""
        val = val.upper()

        if val in ("LOWER_THAN_REQUIRED", "LOWER"):
            return RecommendationAction.LEVEL_GAP

        if val in ("RELATED_FIELD", "UNRELATED_FIELD", "PARTIAL"):
            return RecommendationAction.PARTIAL

        return RecommendationAction.NO_ACTION
