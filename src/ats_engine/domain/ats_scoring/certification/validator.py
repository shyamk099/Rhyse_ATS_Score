"""CertificationScoreValidator definition.

Purpose:
    Provide strict, read-only validation of MatchResults within the Certification domain.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules
from ats_engine.domain.ats_scoring.exceptions import CertificationValidationError
from ats_engine.domain.ats_scoring.certification.resolver import CertificationClassificationResolver


class CertificationScoreValidator:
    """Read-only validator verifying integrity of Certification MatchResults."""

    @staticmethod
    def validate(
        results: Sequence[MatchResult],
        rules: CertificationScoringRules,
    ) -> None:
        """Inspect and validate match results.

        Raises:
            CertificationValidationError: On validation rules failure.
        """
        if results is None:
            raise CertificationValidationError("Results collection cannot be None.")

        seen_pairs = set()

        for result in results:
            # Null metadata check
            if getattr(result, "metadata", None) is None:
                raise CertificationValidationError(f"MatchResult {getattr(result, 'match_id', '')} has null metadata.")

            # Supported match type/matcher category check
            matcher_type = getattr(result, "matcher_type", None)
            if matcher_type != "CertificationMatcher":
                raise CertificationValidationError(
                    f"Unsupported match type: expected 'CertificationMatcher', got '{matcher_type}'."
                )

            # Duplicate certification matches check
            r_id = getattr(result, "resume_feature_id", None)
            j_id = getattr(result, "job_feature_id", None)
            if not r_id or not j_id:
                raise CertificationValidationError(
                    f"MatchResult {getattr(result, 'match_id', '')} is missing feature identifiers."
                )

            pair = (r_id, j_id)
            if pair in seen_pairs:
                raise CertificationValidationError(
                    f"Duplicate certification match detected for Resume Feature '{r_id}' and Job Feature '{j_id}'."
                )
            seen_pairs.add(pair)

            # Check supported classification
            resolver = CertificationClassificationResolver()
            try:
                resolver.validate(result)
            except ValueError as e:
                raise CertificationValidationError(str(e))
