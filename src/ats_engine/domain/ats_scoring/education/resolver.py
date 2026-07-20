"""EducationClassificationResolver definition.

Purpose:
    Provide mapping from MatchResult metadata characteristics into stable internal education classifications.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.interfaces import AbstractClassificationResolver


class EducationClassification(str, Enum):
    """Stable internal types of education match classification."""

    EXACT_MATCH = "EXACT_MATCH"
    HIGHER_THAN_REQUIRED = "HIGHER_THAN_REQUIRED"
    LOWER_THAN_REQUIRED = "LOWER_THAN_REQUIRED"
    RELATED_FIELD = "RELATED_FIELD"
    UNRELATED_FIELD = "UNRELATED_FIELD"
    NO_MATCH = "NO_MATCH"


class EducationClassificationResolver(AbstractClassificationResolver[EducationClassification]):
    """Insulates EducationScorer from Book 05 metadata representations."""

    def resolve(self, result: MatchResult) -> EducationClassification:
        """Resolve EducationClassification type from MatchResult parameters."""
        meta = getattr(result, "metadata", None)
        if not meta:
            return EducationClassification.NO_MATCH

        custom_attrs = getattr(meta, "custom_attributes", {}) or {}
        
        # Check standard custom attribute fields
        val = custom_attrs.get("match_type") or custom_attrs.get("classification")
        if not val:
            return EducationClassification.NO_MATCH
        
        return EducationClassification(val.upper())

    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""
        try:
            classification = self.resolve(result)
        except ValueError as e:
            raise ValueError(f"Invalid education classification: {e}")
        if classification.value not in self.supported_classifications():
            raise ValueError(f"Unsupported education classification: {classification.value}")

    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""
        return [c.value for c in EducationClassification]
