"""Concrete FeatureMatcher implementation for Project features.

Purpose:
    Compare Resume and Job Project features deterministically based on canonical identifiers
    and progressive structural precedence.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import MatchingContext, MatchResult
from ats_engine.domain.matching.project.builder import ProjectMatchBuilder
from ats_engine.domain.matching.project.candidate_builder import ProjectMatchCandidateBuilder
from ats_engine.domain.matching.project.normalizer import ProjectMatchNormalizer
from ats_engine.domain.matching.project.rules import ProjectMatchingRules
from ats_engine.domain.matching.project.stats_builder import ProjectMatchStatisticsBuilder
from ats_engine.domain.matching.project.validator import ProjectMatchValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ProjectMatcher(FeatureMatcher):
    """Matcher performing identifier comparison checks across Resume and Job Projects."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize matcher with structural validation/normalizer dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = ProjectMatchValidator(self._logger)
        self._normalizer = ProjectMatchNormalizer()

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across Resume and Job Description project features.

        Args:
            resume_features: Consolidated Sequence of Resume Features.
            job_features: Consolidated Sequence of Job Description Features.
            context: Governing MatchingContext DTO.

        Returns:
            A sequence of deterministically sorted MatchResult DTOs.
        """
        start_time = time.perf_counter()

        # 1. Resolve Rules
        rules_payload = context.rule_payload.get("project_matching_rules")
        if isinstance(rules_payload, dict):
            rules = ProjectMatchingRules(**rules_payload)
        else:
            rules = ProjectMatchingRules()

        if not rules.enabled:
            return []

        # 2. Build candidates
        candidates = ProjectMatchCandidateBuilder.build_candidates(
            resume_features,
            job_features,
            rules,
        )

        results: list[MatchResult] = []
        validation_failures = 0
        skipped_candidates = 0  # Candidate builder already filtered empties

        for candidate in candidates:
            # 3. Validate Candidate
            errors = self._validator.validate(candidate, rules)
            if errors:
                self._logger.warning(
                    "project_matcher_candidate_validation_failed",
                    extra={"errors": errors},
                )
                validation_failures += 1
                continue

            # 4. Normalize Candidate
            norm_cand = self._normalizer.normalize(candidate, rules)

            rf = norm_cand.resume_feature
            jf = norm_cand.job_feature

            r_id = rf.provenance.source_entity_id
            j_id = jf.provenance.source_entity_id

            is_match = False

            # Precedence 1: Canonical ID match
            if r_id and j_id and r_id == j_id:
                is_match = True
            else:
                # Structural comparisons based on configured mode
                r_val = rf.value or {}
                j_val = jf.value or {}

                proj_name_r = r_val.get("project_name")
                proj_name_j = j_val.get("project_name")
                org_r = r_val.get("organization")
                org_j = j_val.get("organization")
                role_r = r_val.get("role")
                role_j = j_val.get("role")

                mode = rules.comparison_mode

                if mode == "NAME_ORG_ROLE":
                    if (
                        proj_name_r and proj_name_j and proj_name_r.lower().strip() == proj_name_j.lower().strip()
                        and org_r and org_j and org_r.lower().strip() == org_j.lower().strip()
                        and role_r and role_j and role_r.lower().strip() == role_j.lower().strip()
                    ):
                        is_match = True
                elif mode == "NAME_ROLE":
                    if (
                        proj_name_r and proj_name_j and proj_name_r.lower().strip() == proj_name_j.lower().strip()
                        and role_r and role_j and role_r.lower().strip() == role_j.lower().strip()
                    ):
                        is_match = True
                elif mode == "NAME":
                    if proj_name_r and proj_name_j and proj_name_r.lower().strip() == proj_name_j.lower().strip():
                        is_match = True
                elif mode == "ALL":
                    # Hierarchical fallback: try most specific to least
                    if (
                        proj_name_r and proj_name_j and org_r and org_j and role_r and role_j and
                        proj_name_r.lower().strip() == proj_name_j.lower().strip() and
                        org_r.lower().strip() == org_j.lower().strip() and
                        role_r.lower().strip() == role_j.lower().strip()
                    ):
                        is_match = True
                    elif (
                        proj_name_r and proj_name_j and role_r and role_j and
                        proj_name_r.lower().strip() == proj_name_j.lower().strip() and
                        role_r.lower().strip() == role_j.lower().strip()
                    ):
                        is_match = True
                    elif proj_name_r and proj_name_j and proj_name_r.lower().strip() == proj_name_j.lower().strip():
                        is_match = True

            if is_match:
                match_res = ProjectMatchBuilder.build(norm_cand, context)
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
        stats = ProjectMatchStatisticsBuilder.build(
            total_resume_features=len(resume_features),
            total_job_features=len(job_features),
            candidate_pairs=len(candidates),
            matched_pairs=len(sorted_results),
            skipped_candidates=skipped_candidates,
            validation_failures=validation_failures,
            comparison_mode=rules.comparison_mode,
            execution_duration_ms=duration_ms,
        )
        self._logger.info(
            "project_matcher_execution_completed",
            extra={"stats": stats},
        )

        return sorted_results
