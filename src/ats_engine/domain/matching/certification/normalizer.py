"""Structural normalizer for Certification matching candidates.

Purpose:
    Perform read-only normalization on copied certification values without modifying originals.
"""

from __future__ import annotations

import re

from ats_engine.domain.matching.certification.candidate_builder import CertificationMatchCandidate
from ats_engine.domain.matching.certification.rules import CertificationMatchingRules


class CertificationMatchNormalizer:
    """Normalizer for CertificationMatchCandidate attributes."""

    def normalize(
        self,
        candidate: CertificationMatchCandidate,
        rules: CertificationMatchingRules,
    ) -> CertificationMatchCandidate:
        """Perform whitespace collapsing and string trimming in copies of features."""
        if not rules.normalization:
            return candidate

        rf = candidate.resume_feature
        jf = candidate.job_feature

        def norm_val(val: dict) -> dict:
            new_val = dict(val)
            for k in ["certification_name", "issuing_organization"]:
                if k in new_val and isinstance(new_val[k], str):
                    new_val[k] = re.sub(r"\s+", " ", new_val[k]).strip()
            return new_val

        rf_copy = rf.model_copy(update={"value": norm_val(rf.value)})
        jf_copy = jf.model_copy(update={"value": norm_val(jf.value)})

        return CertificationMatchCandidate(
            resume_feature=rf_copy,
            job_feature=jf_copy,
        )
