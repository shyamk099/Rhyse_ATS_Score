"""Candidate pair builder for Certification features.

Purpose:
    Filter input features down to FeatureCategory.CERTIFICATION, filter out empty records,
    and pair them into CertificationMatchCandidate structures.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict

from ats_engine.domain.feature_engineering.models import Feature, FeatureCategory
from ats_engine.domain.matching.certification.rules import CertificationMatchingRules


class CertificationMatchCandidate(BaseModel):
    """Immutable model representing a candidate resume-job certification pair for matching evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    resume_feature: Feature
    job_feature: Feature


class CertificationMatchCandidateBuilder:
    """Builder constructing candidate pairs restricted strictly to Certification features."""

    @classmethod
    def _is_empty_certification(cls, feature: Feature) -> bool:
        """Check if all matching fields (certification_name, issuing_organization) are None or empty."""
        val = feature.value or {}
        name = val.get("certification_name")
        org = val.get("issuing_organization")
        return not any(str(x).strip() for x in [name, org] if x is not None)

    @classmethod
    def build_candidates(
        cls,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        rules: CertificationMatchingRules,
    ) -> Sequence[CertificationMatchCandidate]:
        """Construct candidate pairs from resume and job certification features.

        Args:
            resume_features: Sequence of Resume Feature objects.
            job_features: Sequence of Job Description Feature objects.
            rules: Governing CertificationMatchingRules configuration.

        Returns:
            A sequence of constructed CertificationMatchCandidate instances.
        """
        if not rules.enabled:
            return []

        res_cert = [f for f in resume_features if f.category == FeatureCategory.CERTIFICATION]
        job_cert = [f for f in job_features if f.category == FeatureCategory.CERTIFICATION]

        candidates: list[CertificationMatchCandidate] = []
        for r_feat in res_cert:
            if cls._is_empty_certification(r_feat):
                continue
            for j_feat in job_cert:
                if cls._is_empty_certification(j_feat):
                    continue
                candidates.append(
                    CertificationMatchCandidate(
                        resume_feature=r_feat,
                        job_feature=j_feat,
                    )
                )
        return candidates
