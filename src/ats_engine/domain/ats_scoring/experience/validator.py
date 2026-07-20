"""ExperienceScoreValidator definition.

Purpose:
    Provide strict, read-only validation of MatchResults within the Experience domain.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules
from ats_engine.domain.ats_scoring.exceptions import ExperienceValidationError
from ats_engine.domain.ats_scoring.experience.resolver import ExperienceClassificationResolver


class ExperienceScoreValidator:
    """Read-only validator verifying integrity of Experience MatchResults."""

    @staticmethod
    def validate(
        results: Sequence[MatchResult],
        rules: ExperienceScoringRules,
    ) -> None:
        """Inspect and validate match results.

        Raises:
            ExperienceValidationError: On validation rules failure.
        """
        if results is None:
            raise ExperienceValidationError("Results collection cannot be None.")

        seen_pairs = set()

        for result in results:
            # Null metadata check
            if getattr(result, "metadata", None) is None:
                raise ExperienceValidationError(f"MatchResult {getattr(result, 'match_id', '')} has null metadata.")

            # Supported match type/matcher category check
            matcher_type = getattr(result, "matcher_type", None)
            if matcher_type != "ExperienceMatcher":
                raise ExperienceValidationError(
                    f"Unsupported match type: expected 'ExperienceMatcher', got '{matcher_type}'."
                )

            # Duplicate experience matches check
            r_id = getattr(result, "resume_feature_id", None)
            j_id = getattr(result, "job_feature_id", None)
            if not r_id or not j_id:
                raise ExperienceValidationError(
                    f"MatchResult {getattr(result, 'match_id', '')} is missing feature identifiers."
                )

            pair = (r_id, j_id)
            if pair in seen_pairs:
                raise ExperienceValidationError(
                    f"Duplicate experience match detected for Resume Feature '{r_id}' and Job Feature '{j_id}'."
                )
            seen_pairs.add(pair)

            # Check supported classification
            resolver = ExperienceClassificationResolver()
            try:
                resolver.validate(result)
            except ValueError as e:
                raise ExperienceValidationError(str(e))
