"""CertificationRecommendationRules definition.

Purpose:
    Define deterministic rules evaluating certification elements into recommendation actions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from ats_engine.domain.recommendation.providers.base import RecommendationAction

if TYPE_CHECKING:
    from ats_engine.domain.matching.models import MatchResult


class CertificationRecommendationRules:
    """Deterministic rules evaluating certification elements into recommendation actions.

    Rule Mappings:
        Exact Match              -> NO_ACTION
        Equivalent Certification -> NO_ACTION
        Related Certification    -> PARTIAL
        Partial Match            -> PARTIAL
        Expired Certification    -> EXPIRED
        Missing Certification    -> MISSING
    """

    def evaluate_missing(self, name: str) -> RecommendationAction:
        """Determine action for a missing certification requirement.

        Args:
            name: The certification requirement name.

        Returns:
            MISSING recommendation action.
        """
        if not name or name.strip() == "":
            return RecommendationAction.NO_ACTION
        return RecommendationAction.MISSING

    def evaluate_match(self, match: MatchResult) -> RecommendationAction:
        """Determine action for a matched certification requirement.

        Args:
            match: The MatchResult object.

        Returns:
            The resolved RecommendationAction.
        """
        attrs = getattr(match.metadata, "custom_attributes", {}) or {}
        val = attrs.get("match_type") or attrs.get("classification") or ""
        val = val.upper()

        if val in ("EXPIRED_CERTIFICATION", "EXPIRED"):
            return RecommendationAction.EXPIRED

        if val in ("RELATED_CERTIFICATION", "PARTIAL_MATCH", "RELATED", "PARTIAL"):
            return RecommendationAction.PARTIAL

        return RecommendationAction.NO_ACTION
