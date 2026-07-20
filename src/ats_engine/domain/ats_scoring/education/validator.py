"""EducationScoreValidator definition.

Purpose:
    Provide strict, read-only validation of MatchResults within the Education domain.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules
from ats_engine.domain.ats_scoring.exceptions import EducationValidationError
from ats_engine.domain.ats_scoring.education.resolver import EducationClassificationResolver


class EducationScoreValidator:
    """Read-only validator verifying integrity of Education MatchResults."""

    @staticmethod
    def validate(
        results: Sequence[MatchResult],
        rules: EducationScoringRules,
    ) -> None:
        """Inspect and validate match results.

        Raises:
            EducationValidationError: On validation rules failure.
        """
        if results is None:
            raise EducationValidationError("Results collection cannot be None.")

        seen_pairs = set()

        for result in results:
            # Null metadata check
            if getattr(result, "metadata", None) is None:
                raise EducationValidationError(f"MatchResult {getattr(result, 'match_id', '')} has null metadata.")

            # Supported match type/matcher category check
            matcher_type = getattr(result, "matcher_type", None)
            if matcher_type != "EducationMatcher":
                raise EducationValidationError(
                    f"Unsupported match type: expected 'EducationMatcher', got '{matcher_type}'."
                )

            # Duplicate education matches check
            r_id = getattr(result, "resume_feature_id", None)
            j_id = getattr(result, "job_feature_id", None)
            if not r_id or not j_id:
                raise EducationValidationError(
                    f"MatchResult {getattr(result, 'match_id', '')} is missing feature identifiers."
                )

            pair = (r_id, j_id)
            if pair in seen_pairs:
                raise EducationValidationError(
                    f"Duplicate education match detected for Resume Feature '{r_id}' and Job Feature '{j_id}'."
                )
            seen_pairs.add(pair)

            # Check supported classification
            resolver = EducationClassificationResolver()
            try:
                resolver.validate(result)
            except ValueError as e:
                raise EducationValidationError(str(e))

