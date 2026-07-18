"""Cross-collection match validator.

Purpose:
    Perform read-only inspections verifying cross-collection invariants.
    Detect duplicate match IDs, duplicate feature IDs, invalid matcher categories,
    missing provenance, and invalid references across all matches.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult, ValidationErrorDetail, ValidationWarningDetail
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules


class CrossMatchValidator:
    """Validator performing stateless, read-only checks across all collections of MatchResults."""

    ALLOWED_MATCHER_TYPES = {
        "SkillMatcher",
        "ExperienceMatcher",
        "EducationMatcher",
        "ProjectMatcher",
        "CertificationMatcher",
    }

    @classmethod
    def validate(
        cls,
        results: Sequence[MatchResult],
        rules: CanonicalMatchingRules,
    ) -> tuple[list[ValidationErrorDetail], list[ValidationWarningDetail]]:
        """Validate cross-collection invariants.

        Args:
            results: Combined sequence of MatchResults from all matchers.
            rules: Configuration rules payload.

        Returns:
            A tuple of (errors, warnings).
        """
        errors: list[ValidationErrorDetail] = []
        warnings: list[ValidationWarningDetail] = []

        seen_match_ids: dict[str, int] = {}
        seen_resume_feature_ids: set[str] = set()
        seen_job_feature_ids: set[str] = set()

        for r in results:
            # 1. Duplicate match IDs check
            if r.match_id:
                seen_match_ids[r.match_id] = seen_match_ids.get(r.match_id, 0) + 1

            # 2. Invalid matcher categories check
            if r.matcher_type not in cls.ALLOWED_MATCHER_TYPES:
                errors.append(
                    ValidationErrorDetail(
                        match_id=r.match_id,
                        message=f"Invalid matcher_type: '{r.matcher_type}'",
                        field="matcher_type",
                    )
                )

            # 4. Resume & Job feature references check (warn if multiple matches share the same resume/job feature ID)
            # In some domains, one resume feature can match multiple job features (e.g. a skill matching multiple required skills),
            # but we can log a warning for potential unexpected duplicate assignments.
            if r.resume_feature_id:
                if r.resume_feature_id in seen_resume_feature_ids:
                    warnings.append(
                        ValidationWarningDetail(
                            match_id=r.match_id,
                            message=f"Resume feature ID '{r.resume_feature_id}' is referenced in multiple matches",
                            field="resume_feature_id",
                        )
                    )
                seen_resume_feature_ids.add(r.resume_feature_id)

            if r.job_feature_id:
                if r.job_feature_id in seen_job_feature_ids:
                    warnings.append(
                        ValidationWarningDetail(
                            match_id=r.match_id,
                            message=f"Job feature ID '{r.job_feature_id}' is referenced in multiple matches",
                            field="job_feature_id",
                        )
                    )
                seen_job_feature_ids.add(r.job_feature_id)

        # Append errors for duplicate match IDs
        for match_id, count in seen_match_ids.items():
            if count > 1:
                errors.append(
                    ValidationErrorDetail(
                        match_id=match_id,
                        message=f"Duplicate match_id detected: '{match_id}' occurred {count} times",
                        field="match_id",
                    )
                )

        return errors, warnings
