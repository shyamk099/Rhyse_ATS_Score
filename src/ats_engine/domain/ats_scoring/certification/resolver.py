"""CertificationClassificationResolver definition.

Purpose:
    Provide mapping from MatchResult metadata characteristics into stable internal certification classifications.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.interfaces import AbstractClassificationResolver


class CertificationClassification(str, Enum):
    """Stable internal types of certification match classification."""

    EXACT_MATCH = "EXACT_MATCH"
    EQUIVALENT_CERTIFICATION = "EQUIVALENT_CERTIFICATION"
    RELATED_CERTIFICATION = "RELATED_CERTIFICATION"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    EXPIRED_CERTIFICATION = "EXPIRED_CERTIFICATION"
    NO_MATCH = "NO_MATCH"


class CertificationClassificationResolver(AbstractClassificationResolver[CertificationClassification]):
    """Insulates CertificationScorer from Book 05 metadata representations."""

    def resolve(self, result: MatchResult) -> CertificationClassification:
        """Resolve CertificationClassification type from MatchResult parameters."""
        meta = getattr(result, "metadata", None)
        if not meta:
            return CertificationClassification.NO_MATCH

        custom_attrs = getattr(meta, "custom_attributes", {}) or {}
        
        # Check standard custom attribute fields
        val = custom_attrs.get("match_type") or custom_attrs.get("classification")
        if not val:
            return CertificationClassification.NO_MATCH
        
        return CertificationClassification(val.upper())

    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""
        try:
            classification = self.resolve(result)
        except ValueError as e:
            raise ValueError(f"Invalid certification classification: {e}")
        if classification.value not in self.supported_classifications():
            raise ValueError(f"Unsupported certification classification: {classification.value}")

    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""
        return [c.value for c in CertificationClassification]
