"""Structural normalizer for Education matching candidates.

Purpose:
    Perform read-only normalization (casing, trimming, and whitespace collapsing)
    on copied education values without modifying the original features in the source collections.
"""

from __future__ import annotations

import re

from ats_engine.domain.matching.education.candidate_builder import EducationMatchCandidate
from ats_engine.domain.matching.education.rules import EducationMatchingRules


class EducationMatchNormalizer:
    """Normalizer for EducationMatchCandidate attributes."""

    def normalize(
        self,
        candidate: EducationMatchCandidate,
        rules: EducationMatchingRules,
    ) -> EducationMatchCandidate:
        """Perform whitespace collapsing and string trimming in copies of features.

        Args:
            candidate: Candidate pair under normalization.
            rules: Active EducationMatchingRules config.

        Returns:
            A new EducationMatchCandidate with normalized feature values.
        """
        if not rules.normalization:
            return candidate

        rf = candidate.resume_feature
        jf = candidate.job_feature

        # Helper to normalize dict string fields
        def norm_val(val: dict) -> dict:
            new_val = dict(val)
            for k in ["institution", "degree", "major", "specialization"]:
                if k in new_val and isinstance(new_val[k], str):
                    new_val[k] = re.sub(r"\s+", " ", new_val[k]).strip()
            return new_val

        # Update values in copies
        rf_copy = rf.model_copy(update={"value": norm_val(rf.value)})
        jf_copy = jf.model_copy(update={"value": norm_val(jf.value)})

        return EducationMatchCandidate(
            resume_feature=rf_copy,
            job_feature=jf_copy,
        )
