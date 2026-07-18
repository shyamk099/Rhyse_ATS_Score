"""Structural normalizer for Skill matching candidates.

Purpose:
    Perform read-only normalization (casing, trimming, and whitespace collapsing)
    without modifying the original features in the source collections.
"""

from __future__ import annotations

import re

from ats_engine.domain.matching.skill.candidate_builder import SkillMatchCandidate
from ats_engine.domain.matching.skill.rules import SkillMatchingRules


class SkillMatchNormalizer:
    """Normalizer for SkillMatchCandidate attributes."""

    def normalize(
        self,
        candidate: SkillMatchCandidate,
        rules: SkillMatchingRules,
    ) -> SkillMatchCandidate:
        """Perform whitespace collapsing and name trimming in copies of features.

        Args:
            candidate: Candidate pair under normalization.
            rules: Active SkillMatchingRules config.

        Returns:
            A new SkillMatchCandidate with normalized feature values.
        """
        if not rules.normalization:
            return candidate

        rf = candidate.resume_feature
        jf = candidate.job_feature

        # Collapse whitespace and trim
        rf_name_norm = re.sub(r"\s+", " ", rf.name).strip()
        jf_name_norm = re.sub(r"\s+", " ", jf.name).strip()

        # Update in copies to preserve original features immutability
        rf_copy = rf.model_copy(update={"name": rf_name_norm})
        jf_copy = jf.model_copy(update={"name": jf_name_norm})

        return SkillMatchCandidate(
            resume_feature=rf_copy,
            job_feature=jf_copy,
        )
