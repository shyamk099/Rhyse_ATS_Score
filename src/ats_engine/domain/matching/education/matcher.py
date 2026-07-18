"""Concrete FeatureMatcher implementation for Education features.

Purpose:
    Compare Resume and Job Education features based on canonical IDs and precedence rules
    using shared comparison utilities.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.common.comparison import (
    compare_matching_fields,
    safe_compare_strings,
)
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import MatchingContext, MatchResult
from ats_engine.domain.matching.education.builder import EducationMatchBuilder
from ats_engine.domain.matching.education.candidate_builder import EducationMatchCandidateBuilder
from ats_engine.domain.matching.education.normalizer import EducationMatchNormalizer
from ats_engine.domain.matching.education.rules import EducationMatchingRules
from ats_engine.domain.matching.education.stats_builder import EducationMatchStatisticsBuilder
from ats_engine.domain.matching.education.validator import EducationMatchValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class EducationMatcher(FeatureMatcher):
    """Matcher performing precedence checks across Resume and Job Education features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize matcher with structural validation/normalizer dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = EducationMatchValidator(self._logger)
        self._normalizer = EducationMatchNormalizer()

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across Resume and Job Description education features.

        Args:
            resume_features: Consolidated Sequence of Resume Features.
            job_features: Consolidated Sequence of Job Description Features.
            context: Governing MatchingContext DTO.

        Returns:
            A sequence of deterministically sorted MatchResult DTOs.
        """
        start_time = time.perf_counter()

        # 1. Resolve Rules
        rules_payload = context.rule_payload.get("education_matching_rules")
        if isinstance(rules_payload, dict):
            rules = EducationMatchingRules(**rules_payload)
        else:
            rules = EducationMatchingRules()

        if not rules.enabled:
            return []

        # 2. Build candidates
        candidates = EducationMatchCandidateBuilder.build_candidates(
            resume_features,
            job_features,
            rules,
        )

        results: list[MatchResult] = []
        validation_failures = 0

        for candidate in candidates:
            # 3. Validate Candidate
            errors = self._validator.validate(candidate, rules)
            if errors:
                self._logger.warning(
                    "education_matcher_candidate_validation_failed",
                    extra={"errors": errors},
                )
                validation_failures += 1
                continue

            # 4. Normalize Candidate (copies created inside normalizer to leave originals unmutated)
            norm_cand = self._normalizer.normalize(candidate, rules)

            rf = norm_cand.resume_feature
            jf = norm_cand.job_feature

            r_id = rf.provenance.source_entity_id
            j_id = jf.provenance.source_entity_id

            is_match = False

            # Precedence rule 1: Canonical ID check
            if r_id and j_id:
                if r_id == j_id:
                    is_match = True
            else:
                # Bypassed lower checks if both contain different IDs (mismatch constraint)
                # If either or both missing canonical ID, evaluate structural properties
                r_val = rf.value or {}
                j_val = jf.value or {}

                # Precedence rule 2: Institution + Degree + Major + Specialization
                if not is_match and rules.comparison_mode in ("ALL", "INSTITUTION_DEGREE_MAJOR_SPECIALIZATION"):
                    if compare_matching_fields(r_val, j_val, ["institution", "degree", "major", "specialization"]):
                        is_match = True

                # Precedence rule 3: Institution + Degree + Major
                if not is_match and rules.comparison_mode in ("ALL", "INSTITUTION_DEGREE_MAJOR"):
                    if compare_matching_fields(r_val, j_val, ["institution", "degree", "major"]):
                        is_match = True

                # Precedence rule 4: Institution + Degree
                if not is_match and rules.comparison_mode in ("ALL", "INSTITUTION_DEGREE"):
                    if compare_matching_fields(r_val, j_val, ["institution", "degree"]):
                        is_match = True

            if is_match:
                match_res = EducationMatchBuilder.build(norm_cand, context)
                results.append(match_res)

        # 5. Sort results deterministically
        if rules.deterministic_ordering:
            sorted_results = sorted(
                results,
                key=lambda r: (r.matcher_type, r.resume_feature_id, r.job_feature_id),
            )
        else:
            sorted_results = results

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        stats = EducationMatchStatisticsBuilder.build(
            total_resume_features=len(resume_features),
            total_job_features=len(job_features),
            candidate_pairs=len(candidates),
            matched_pairs=len(sorted_results),
            skipped_candidates=0,
            validation_failures=validation_failures,
            comparison_mode=rules.comparison_mode,
            execution_duration_ms=duration_ms,
        )

        self._logger.info(
            "education_matcher_execution_completed",
            extra={"stats": stats},
        )

        return sorted_results
