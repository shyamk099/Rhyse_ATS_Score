"""Skill candidate validator.

Purpose:
    Perform basic sanity validation on matched skill candidates.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.skills.skill_models import SkillCandidate
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class SkillCandidateValidator:
    """Stateless validator auditing matching text lengths and scopes."""

    @classmethod
    def validate(cls, candidate: SkillCandidate, rules: SkillExtractionRules) -> bool:
        """Validate candidate structure.

        Args:
            candidate: Discovered candidate.
            rules: Extraction rule guidelines.

        Returns:
            True if candidate is valid, False otherwise.
        """
        text = candidate.matched_text.strip()
        if not text:
            return False

        # Match must be mapped within active rule dictionary keys
        if candidate.skill_id not in rules.dictionary:
            return False

        return True
