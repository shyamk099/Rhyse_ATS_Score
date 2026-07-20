"""ProjectClassificationResolver definition.

Purpose:
    Provide mapping from MatchResult metadata characteristics into stable internal project classifications.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.interfaces import AbstractClassificationResolver


class ProjectClassification(str, Enum):
    """Stable internal types of project match classification."""

    EXACT_MATCH = "EXACT_MATCH"
    SIMILAR_PROJECT = "SIMILAR_PROJECT"
    RELATED_PROJECT = "RELATED_PROJECT"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"


class ProjectClassificationResolver(AbstractClassificationResolver[ProjectClassification]):
    """Insulates ProjectScorer from Book 05 metadata representations."""

    def resolve(self, result: MatchResult) -> ProjectClassification:
        """Resolve ProjectClassification type from MatchResult parameters."""
        meta = getattr(result, "metadata", None)
        if not meta:
            return ProjectClassification.NO_MATCH

        custom_attrs = getattr(meta, "custom_attributes", {}) or {}
        
        # Check standard custom attribute fields
        val = custom_attrs.get("match_type") or custom_attrs.get("classification")
        if not val:
            return ProjectClassification.NO_MATCH
        
        return ProjectClassification(val.upper())

    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""
        try:
            classification = self.resolve(result)
        except ValueError as e:
            raise ValueError(f"Invalid project classification: {e}")
        if classification.value not in self.supported_classifications():
            raise ValueError(f"Unsupported project classification: {classification.value}")

    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""
        return [c.value for c in ProjectClassification]
