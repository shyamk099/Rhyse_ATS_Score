"""Structural normalizer for Project matching candidates.

Purpose:
    Perform read-only normalization on copied project values without modifying originals.
"""

from __future__ import annotations

import re

from ats_engine.domain.matching.project.candidate_builder import ProjectMatchCandidate
from ats_engine.domain.matching.project.rules import ProjectMatchingRules


class ProjectMatchNormalizer:
    """Normalizer for ProjectMatchCandidate attributes."""

    def normalize(
        self,
        candidate: ProjectMatchCandidate,
        rules: ProjectMatchingRules,
    ) -> ProjectMatchCandidate:
        """Perform whitespace collapsing and string trimming in copies of features."""
        if not rules.normalization:
            return candidate

        rf = candidate.resume_feature
        jf = candidate.job_feature

        def norm_val(val: dict) -> dict:
            new_val = dict(val)
            for k in ["project_name", "organization", "role"]:
                if k in new_val and isinstance(new_val[k], str):
                    new_val[k] = re.sub(r"\s+", " ", new_val[k]).strip()
            return new_val

        rf_copy = rf.model_copy(update={"value": norm_val(rf.value)})
        jf_copy = jf.model_copy(update={"value": norm_val(jf.value)})

        return ProjectMatchCandidate(
            resume_feature=rf_copy,
            job_feature=jf_copy,
        )
