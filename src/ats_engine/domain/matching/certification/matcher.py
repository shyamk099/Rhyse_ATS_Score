"""Concrete FeatureMatcher implementation for Certification features.

Purpose:
    Compare Resume and Job Certification features deterministically based on canonical identifiers
    and progressive structural precedence.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import MatchingContext, MatchResult
from ats_engine.domain.matching.certification.builder import CertificationMatchBuilder
from ats_engine.domain.matching.certification.candidate_builder import CertificationMatchCandidateBuilder
from ats_engine.domain.matching.certification.normalizer import CertificationMatchNormalizer
from ats_engine.domain.matching.certification.rules import CertificationMatchingRules
from ats_engine.domain.matching.certification.stats_builder import CertificationMatchStatisticsBuilder
from ats_engine.domain.matching.certification.validator import CertificationMatchValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CertificationMatcher(FeatureMatcher):
    """Matcher performing identifier comparison checks across Resume and Job Certifications."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize matcher with structural validation/normalizer dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = CertificationMatchValidator(self._logger)
        self._normalizer = CertificationMatchNormalizer()

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across Resume and Job Description certification features.

        Args:
            resume_features: Consolidated Sequence of Resume Features.
            job_features: Consolidated Sequence of Job Description Features.
            context: Governing MatchingContext DTO.

        Returns:
            A sequence of deterministically sorted MatchResult DTOs.
        """
        start_time = time.perf_counter()

        # 1. Resolve Rules
        rules_payload = context.rule_payload.get("certification_matching_rules")
        if isinstance(rules_payload, dict):
            rules = CertificationMatchingRules(**rules_payload)
        else:
            rules = CertificationMatchingRules()

        if not rules.enabled:
            return []

        # 2. Build candidates
        candidates = CertificationMatchCandidateBuilder.build_candidates(
            resume_features,
            job_features,
            rules,
        )

        results: list[MatchResult] = []
        validation_failures = 0
        skipped_candidates = 0  # already filtered by builder

        for candidate in candidates:
            # 3. Validate Candidate
            errors = self._validator.validate(candidate, rules)
            if errors:
                self._logger.warning(
                    "certification_matcher_candidate_validation_failed",
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
                # Structural comparisons based on mode
                r_val = rf.value or {}
                j_val = jf.value or {}

                name_r = r_val.get("certification_name")
                name_j = j_val.get("certification_name")
                org_r = r_val.get("issuing_organization")
                org_j = j_val.get("issuing_organization")

                mode = rules.comparison_mode

                if mode == "NAME_ORG":
                    if (
                        name_r and name_j and name_r.lower().strip() == name_j.lower().strip()
                        and org_r and org_j and org_r.lower().strip() == org_j.lower().strip()
                    ):
                        is_match = True
                elif mode == "NAME":
                    if name_r and name_j and name_r.lower().strip() == name_j.lower().strip():
                        is_match = True
                elif mode == "ALL":
                    if (
                        name_r and name_j and org_r and org_j and
                        name_r.lower().strip() == name_j.lower().strip() and
                        org_r.lower().strip() == org_j.lower().strip()
                    ):
                        is_match = True
                    elif name_r and name_j and name_r.lower().strip() == name_j.lower().strip():
                        is_match = True

            if is_match:
                match_res = CertificationMatchBuilder.build(norm_cand, context)
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
        stats = CertificationMatchStatisticsBuilder.build(
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
            "certification_matcher_execution_completed",
            extra={"stats": stats},
        )

        return sorted_results
