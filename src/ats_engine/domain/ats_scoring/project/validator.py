"""ProjectScoreValidator definition.

Purpose:
    Provide strict, read-only validation of MatchResults within the Project domain.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules
from ats_engine.domain.ats_scoring.exceptions import ProjectValidationError
from ats_engine.domain.ats_scoring.project.resolver import ProjectClassificationResolver


class ProjectScoreValidator:
    """Read-only validator verifying integrity of Project MatchResults."""

    @staticmethod
    def validate(
        results: Sequence[MatchResult],
        rules: ProjectScoringRules,
    ) -> None:
        """Inspect and validate match results.

        Raises:
            ProjectValidationError: On validation rules failure.
        """
        if results is None:
            raise ProjectValidationError("Results collection cannot be None.")

        seen_pairs = set()

        for result in results:
            # Null metadata check
            if getattr(result, "metadata", None) is None:
                raise ProjectValidationError(f"MatchResult {getattr(result, 'match_id', '')} has null metadata.")

            # Supported match type/matcher category check
            matcher_type = getattr(result, "matcher_type", None)
            if matcher_type != "ProjectMatcher":
                raise ProjectValidationError(
                    f"Unsupported match type: expected 'ProjectMatcher', got '{matcher_type}'."
                )

            # Duplicate project matches check
            r_id = getattr(result, "resume_feature_id", None)
            j_id = getattr(result, "job_feature_id", None)
            if not r_id or not j_id:
                raise ProjectValidationError(
                    f"MatchResult {getattr(result, 'match_id', '')} is missing feature identifiers."
                )

            pair = (r_id, j_id)
            if pair in seen_pairs:
                raise ProjectValidationError(
                    f"Duplicate project match detected for Resume Feature '{r_id}' and Job Feature '{j_id}'."
                )
            seen_pairs.add(pair)

            # Check supported classification
            resolver = ProjectClassificationResolver()
            try:
                resolver.validate(result)
            except ValueError as e:
                raise ProjectValidationError(str(e))
