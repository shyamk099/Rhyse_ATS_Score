"""SkillClassificationResolver definition.

Purpose:
    Provide mapping from MatchResult metadata characteristics into stable internal skill classifications.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.interfaces import AbstractClassificationResolver


class SkillClassification(str, Enum):
    """Stable internal types of skill importance."""

    MANDATORY = "MANDATORY"
    OPTIONAL = "OPTIONAL"


class SkillClassificationResolver(AbstractClassificationResolver[SkillClassification]):
    """Insulates SkillScorer from Book 05 metadata representations."""

    def resolve(self, result: MatchResult) -> SkillClassification:
        """Resolve SkillClassification type from MatchResult parameters."""
        meta = getattr(result, "metadata", None)
        if not meta:
            return SkillClassification.OPTIONAL

        custom_attrs = getattr(meta, "custom_attributes", {}) or {}
        is_mandatory = custom_attrs.get("is_mandatory", False) or custom_attrs.get("mandatory", False)
        importance = custom_attrs.get("importance", "")

        if is_mandatory or importance == "mandatory":
            return SkillClassification.MANDATORY

        return SkillClassification.OPTIONAL

    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""
        # Verification checking supported classifications
        try:
            classification = self.resolve(result)
        except ValueError as e:
            raise ValueError(f"Invalid skill classification: {e}")
        if classification.value not in self.supported_classifications():
            raise ValueError(f"Unsupported skill classification: {classification.value}")

    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""
        return [c.value for c in SkillClassification]
