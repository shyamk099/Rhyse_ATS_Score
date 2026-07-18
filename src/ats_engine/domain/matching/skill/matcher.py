"""Concrete FeatureMatcher implementation for Skill features.

Purpose:
    Compare Resume and Job Skill features deterministically based on canonical identifiers.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import MatchingContext, MatchResult
from ats_engine.domain.matching.skill.builder import SkillMatchBuilder
from ats_engine.domain.matching.skill.candidate_builder import SkillMatchCandidateBuilder
from ats_engine.domain.matching.skill.normalizer import SkillMatchNormalizer
from ats_engine.domain.matching.skill.rules import SkillMatchingRules
from ats_engine.domain.matching.skill.stats_builder import SkillMatchStatisticsBuilder
from ats_engine.domain.matching.skill.validator import SkillMatchValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SkillMatcher(FeatureMatcher):
    """Matcher performing identifier comparison checks across Resume and Job Skills."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize matcher with structural validation/normalizer dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = SkillMatchValidator(self._logger)
        self._normalizer = SkillMatchNormalizer()

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across Resume and Job Description skill features.

        Args:
            resume_features: Consolidated Sequence of Resume Features.
            job_features: Consolidated Sequence of Job Description Features.
            context: Governing MatchingContext DTO.

        Returns:
            A sequence of deterministically sorted MatchResult DTOs.
        """
        start_time = time.perf_counter()

        # 1. Resolve Rules
        rules_payload = context.rule_payload.get("skill_matching_rules")
        if isinstance(rules_payload, dict):
            rules = SkillMatchingRules(**rules_payload)
        else:
            rules = SkillMatchingRules()

        if not rules.enabled:
            return []

        # 2. Build candidates
        candidates = SkillMatchCandidateBuilder.build_candidates(
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
                    "skill_matcher_candidate_validation_failed",
                    extra={"errors": errors},
                )
                validation_failures += 1
                continue

            # 4. Normalize Candidate
            norm_cand = self._normalizer.normalize(candidate, rules)

            rf = norm_cand.resume_feature
            jf = norm_cand.job_feature

            # 5. Rule 1 - Exact matching ONLY on canonical IDs
            r_id = rf.provenance.source_entity_id
            j_id = jf.provenance.source_entity_id

            is_match = False
            if rules.comparison_mode == "CANONICAL":
                if r_id and j_id and r_id == j_id:
                    is_match = True
            elif rules.comparison_mode == "ALL":
                # Match on canonical ID, OR match on normalized names if either is raw
                if r_id and j_id:
                    is_match = (r_id == j_id)
                else:
                    # Compare names (case-insensitive strip matching)
                    is_match = (rf.name.lower().strip() == jf.name.lower().strip())

            if is_match:
                match_res = SkillMatchBuilder.build(norm_cand, context)
                results.append(match_res)

        # 6. Sort results deterministically (Rule 7)
        if rules.deterministic_ordering:
            sorted_results = sorted(
                results,
                key=lambda r: (r.matcher_type, r.resume_feature_id, r.job_feature_id),
            )
        else:
            sorted_results = results

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        stats = SkillMatchStatisticsBuilder.build(
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
            "skill_matcher_execution_completed",
            extra={"stats": stats},
        )

        return sorted_results
