"""ExperienceClassificationResolver definition.

Purpose:
    Provide mapping from MatchResult metadata characteristics into stable internal experience classifications.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.interfaces import AbstractClassificationResolver


class ExperienceClassification(str, Enum):
    """Stable internal types of experience match importance/classification."""

    EXACT_MATCH = "EXACT_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    OVERQUALIFIED = "OVERQUALIFIED"
    UNDERQUALIFIED = "UNDERQUALIFIED"
    NO_MATCH = "NO_MATCH"


class ExperienceClassificationResolver(AbstractClassificationResolver[ExperienceClassification]):
    """Insulates ExperienceScorer from Book 05 metadata representations."""

    def resolve(self, result: MatchResult) -> ExperienceClassification:
        """Resolve ExperienceClassification type from MatchResult parameters."""
        meta = getattr(result, "metadata", None)
        if not meta:
            return ExperienceClassification.NO_MATCH

        custom_attrs = getattr(meta, "custom_attributes", {}) or {}
        
        # Check standard custom attribute fields
        val = custom_attrs.get("match_type") or custom_attrs.get("classification")
        if not val:
            return ExperienceClassification.NO_MATCH
        
        return ExperienceClassification(val.upper())

    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""
        try:
            classification = self.resolve(result)
        except ValueError as e:
            raise ValueError(f"Invalid experience classification: {e}")
        if classification.value not in self.supported_classifications():
            raise ValueError(f"Unsupported experience classification: {classification.value}")

    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""
        return [c.value for c in ExperienceClassification]
