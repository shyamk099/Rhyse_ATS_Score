"""SkillScoreValidator definition.

Purpose:
    Provide strict, read-only validation of MatchResults within the Skill domain.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules
from ats_engine.domain.ats_scoring.exceptions import SkillValidationError


class SkillScoreValidator:
    """Read-only validator verifying integrity of Skill MatchResults."""

    @staticmethod
    def validate(
        results: Sequence[MatchResult],
        rules: SkillScoringRules,
    ) -> None:
        """Inspect and validate match results.

        Raises:
            SkillValidationError: On validation rules failure.
        """
        if results is None:
            raise SkillValidationError("Results collection cannot be None.")

        seen_pairs = set()

        for result in results:
            # Null metadata check
            if getattr(result, "metadata", None) is None:
                raise SkillValidationError(f"MatchResult {getattr(result, 'match_id', '')} has null metadata.")

            # Supported match type/matcher category check
            matcher_type = getattr(result, "matcher_type", None)
            if matcher_type != "SkillMatcher":
                raise SkillValidationError(
                    f"Unsupported match type: expected 'SkillMatcher', got '{matcher_type}'."
                )

            # Duplicate skill matches check
            r_id = getattr(result, "resume_feature_id", None)
            j_id = getattr(result, "job_feature_id", None)
            if not r_id or not j_id:
                raise SkillValidationError(
                    f"MatchResult {getattr(result, 'match_id', '')} is missing feature identifiers."
                )

            pair = (r_id, j_id)
            if pair in seen_pairs:
                raise SkillValidationError(
                    f"Duplicate skill match detected for Resume Feature '{r_id}' and Job Feature '{j_id}'."
                )
            seen_pairs.add(pair)
