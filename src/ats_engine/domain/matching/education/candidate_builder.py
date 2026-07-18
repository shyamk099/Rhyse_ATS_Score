"""Candidate pair builder for Education features.

Purpose:
    Filter input features down to FeatureCategory.EDUCATION, filter out empty records,
    and pair them into EducationMatchCandidate structures.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict

from ats_engine.domain.feature_engineering.models import Feature, FeatureCategory
from ats_engine.domain.matching.education.rules import EducationMatchingRules


class EducationMatchCandidate(BaseModel):
    """Immutable model representing a candidate resume-job education pair for matching evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    resume_feature: Feature
    job_feature: Feature


class EducationMatchCandidateBuilder:
    """Builder constructing candidate pairs restricted strictly to Education features."""

    @classmethod
    def _is_empty_education(cls, feature: Feature) -> bool:
        """Check if all matching fields (institution, degree, major, specialization) are None or empty."""
        val = feature.value or {}
        inst = val.get("institution")
        deg = val.get("degree")
        maj = val.get("major")
        spec = val.get("specialization")

        return not any(
            str(x).strip() for x in [inst, deg, maj, spec] if x is not None
        )

    @classmethod
    def build_candidates(
        cls,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        rules: EducationMatchingRules,
    ) -> Sequence[EducationMatchCandidate]:
        """Construct candidate pairs from resume and job education features.

        Args:
            resume_features: Sequence of Resume Feature objects.
            job_features: Sequence of Job Description Feature objects.
            rules: Governing EducationMatchingRules configuration.

        Returns:
            A sequence of constructed EducationMatchCandidate instances.
        """
        if not rules.enabled:
            return []

        # Filter categories
        res_edu = [f for f in resume_features if f.category == FeatureCategory.EDUCATION]
        job_edu = [f for f in job_features if f.category == FeatureCategory.EDUCATION]

        candidates: list[EducationMatchCandidate] = []
        for r_feat in res_edu:
            # Skip empty comparisons (Validation Rule)
            if cls._is_empty_education(r_feat):
                continue
            for j_feat in job_edu:
                if cls._is_empty_education(j_feat):
                    continue
                candidates.append(
                    EducationMatchCandidate(
                        resume_feature=r_feat,
                        job_feature=j_feat,
                    )
                )

        return candidates
