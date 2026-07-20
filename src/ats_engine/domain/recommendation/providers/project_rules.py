"""ProjectRecommendationRules definition.

Purpose:
    Define deterministic rules evaluating project elements into recommendation actions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from ats_engine.domain.recommendation.providers.base import RecommendationAction

if TYPE_CHECKING:
    from ats_engine.domain.matching.models import MatchResult


class ProjectRecommendationRules:
    """Deterministic rules evaluating project elements into recommendation actions.

    Rule Mappings:
        Exact Match       -> NO_ACTION
        Equivalent Match  -> NO_ACTION
        Partial Match     -> PARTIAL
        Similar Project   -> RELATED_GAP
        Related Project   -> RELATED_GAP
        Missing Project   -> MISSING
    """

    def evaluate_missing(self, name: str) -> RecommendationAction:
        """Determine action for a missing project requirement.

        Args:
            name: The project requirement name.

        Returns:
            MISSING recommendation action.
        """
        if not name or name.strip() == "":
            return RecommendationAction.NO_ACTION
        return RecommendationAction.MISSING

    def evaluate_match(self, match: MatchResult) -> RecommendationAction:
        """Determine action for a matched project requirement.

        Args:
            match: The MatchResult object.

        Returns:
            The resolved RecommendationAction.
        """
        attrs = getattr(match.metadata, "custom_attributes", {}) or {}
        val = attrs.get("match_type") or attrs.get("classification") or ""
        val = val.upper()

        if val in ("SIMILAR_PROJECT", "RELATED_PROJECT", "SIMILAR", "RELATED"):
            return RecommendationAction.RELATED_GAP

        if val in ("PARTIAL_MATCH", "PARTIAL"):
            return RecommendationAction.PARTIAL

        return RecommendationAction.NO_ACTION
