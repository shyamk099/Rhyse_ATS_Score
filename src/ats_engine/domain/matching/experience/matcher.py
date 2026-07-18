"""Concrete FeatureMatcher implementation for Experience features.

Purpose:
    Compare Resume and Job Experience features based on canonical IDs and company/title.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import MatchingContext, MatchResult
from ats_engine.domain.matching.experience.builder import ExperienceMatchBuilder
from ats_engine.domain.matching.experience.candidate_builder import ExperienceMatchCandidateBuilder
from ats_engine.domain.matching.experience.normalizer import ExperienceMatchNormalizer
from ats_engine.domain.matching.experience.rules import ExperienceMatchingRules
from ats_engine.domain.matching.experience.stats_builder import ExperienceMatchStatisticsBuilder
from ats_engine.domain.matching.experience.validator import ExperienceMatchValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ExperienceMatcher(FeatureMatcher):
    """Matcher performing comparison checks across Resume and Job Experiences."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize matcher with structural validation/normalizer dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = ExperienceMatchValidator(self._logger)
        self._normalizer = ExperienceMatchNormalizer()

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across Resume and Job Description experience features.

        Args:
            resume_features: Consolidated Sequence of Resume Features.
            job_features: Consolidated Sequence of Job Description Features.
            context: Governing MatchingContext DTO.

        Returns:
            A sequence of deterministically sorted MatchResult DTOs.
        """
        start_time = time.perf_counter()

        # 1. Resolve Rules
        rules_payload = context.rule_payload.get("experience_matching_rules")
        if isinstance(rules_payload, dict):
            rules = ExperienceMatchingRules(**rules_payload)
        else:
            rules = ExperienceMatchingRules()

        if not rules.enabled:
            return []

        # 2. Build candidates
        candidates = ExperienceMatchCandidateBuilder.build_candidates(
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
                    "experience_matcher_candidate_validation_failed",
                    extra={"errors": errors},
                )
                validation_failures += 1
                continue

            # 4. Normalize Candidate (performs copies to leave original Features untouched)
            norm_cand = self._normalizer.normalize(candidate, rules)

            rf = norm_cand.resume_feature
            jf = norm_cand.job_feature

            r_id = rf.provenance.source_entity_id
            j_id = jf.provenance.source_entity_id

            is_match = False

            # Precedence check: Match using canonical ID first if both contain same ID
            if r_id and j_id:
                if r_id == j_id:
                    is_match = True
            else:
                # Fallback to configured comparison mode
                r_val = rf.value or {}
                j_val = jf.value or {}

                r_comp = r_val.get("company")
                j_comp = j_val.get("company")
                r_title = r_val.get("job_title")
                j_title = j_val.get("job_title")

                if rules.comparison_mode == "COMPANY_TITLE":
                    if r_comp and j_comp and r_comp.lower().strip() == j_comp.lower().strip():
                        if r_title and j_title and r_title.lower().strip() == j_title.lower().strip():
                            is_match = True
                elif rules.comparison_mode == "ALL":
                    # Match on company and title
                    if r_comp and j_comp and r_comp.lower().strip() == j_comp.lower().strip():
                        if r_title and j_title and r_title.lower().strip() == j_title.lower().strip():
                            is_match = True

            if is_match:
                match_res = ExperienceMatchBuilder.build(norm_cand, context)
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
        stats = ExperienceMatchStatisticsBuilder.build(
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
            "experience_matcher_execution_completed",
            extra={"stats": stats},
        )

        return sorted_results
