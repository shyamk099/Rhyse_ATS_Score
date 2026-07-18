"""Candidate pair builder for Experience features.

Purpose:
    Filter input features down to FeatureCategory.EXPERIENCE and pair them
    into ExperienceMatchCandidate structures.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict

from ats_engine.domain.feature_engineering.models import Feature, FeatureCategory
from ats_engine.domain.matching.experience.rules import ExperienceMatchingRules


class ExperienceMatchCandidate(BaseModel):
    """Immutable model representing a candidate resume-job experience pair for matching evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    resume_feature: Feature
    job_feature: Feature


class ExperienceMatchCandidateBuilder:
    """Builder constructing candidate pairs restricted strictly to Experience features."""

    @classmethod
    def build_candidates(
        cls,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        rules: ExperienceMatchingRules,
    ) -> Sequence[ExperienceMatchCandidate]:
        """Construct candidate pairs from resume and job experience features.

        Args:
            resume_features: Sequence of Resume Feature objects.
            job_features: Sequence of Job Description Feature objects.
            rules: Governing ExperienceMatchingRules configuration.

        Returns:
            A sequence of constructed ExperienceMatchCandidate instances.
        """
        if not rules.enabled:
            return []

        # Filter categories
        res_exp = [f for f in resume_features if f.category == FeatureCategory.EXPERIENCE]
        job_exp = [f for f in job_features if f.category == FeatureCategory.EXPERIENCE]

        candidates: list[ExperienceMatchCandidate] = []
        for r_feat in res_exp:
            for j_feat in job_exp:
                candidates.append(
                    ExperienceMatchCandidate(
                        resume_feature=r_feat,
                        job_feature=j_feat,
                    )
                )

        return candidates
