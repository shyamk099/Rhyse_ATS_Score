"""Structural validator for individual MatchResults.

Purpose:
    Perform read-only validation inspections on individual MatchResults.
    Never modifies, repairs, or normalizes inputs.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult, ValidationErrorDetail
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules


class MatchValidator:
    """Validator performing stateless, read-only structural checks on individual MatchResults."""

    @classmethod
    def validate(
        cls,
        results: Sequence[MatchResult],
        rules: CanonicalMatchingRules,
    ) -> list[ValidationErrorDetail]:
        """Validate structural compliance of MatchResults.

        Args:
            results: Sequence of MatchResult objects.
            rules: Configuration rules payload.

        Returns:
            List of ValidationErrorDetail describing any issues found.
        """
        errors: list[ValidationErrorDetail] = []
        
        for r in results:
            if not r.match_id or not isinstance(r.match_id, str):
                errors.append(
                    ValidationErrorDetail(
                        match_id=getattr(r, "match_id", "unknown"),
                        message="Missing or invalid match_id",
                        field="match_id",
                    )
                )
            if not r.matcher_type or not isinstance(r.matcher_type, str):
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message="Missing or invalid matcher_type",
                        field="matcher_type",
                    )
                )
            if not r.resume_feature_id or not isinstance(r.resume_feature_id, str):
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message="Missing or invalid resume_feature_id",
                        field="resume_feature_id",
                    )
                )
            if not r.job_feature_id or not isinstance(r.job_feature_id, str):
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message="Missing or invalid job_feature_id",
                        field="job_feature_id",
                    )
                )
            if not r.metadata:
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message="Missing metadata",
                        field="metadata",
                    )
                )
            if not r.provenance:
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message="Missing provenance",
                        field="provenance",
                    )
                )
                
        return errors
