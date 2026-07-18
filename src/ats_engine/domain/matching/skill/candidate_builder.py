"""Candidate pair builder for Skill features.

Purpose:
    Filter input features down to FeatureCategory.SKILL and pair them
    into SkillMatchCandidate structures.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict

from ats_engine.domain.feature_engineering.models import Feature, FeatureCategory
from ats_engine.domain.matching.skill.rules import SkillMatchingRules


class SkillMatchCandidate(BaseModel):
    """Immutable model representing a candidate resume-job skill pair for matching evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    resume_feature: Feature
    job_feature: Feature


class SkillMatchCandidateBuilder:
    """Builder constructing candidate pairs restricted strictly to Skill features."""

    @classmethod
    def build_candidates(
        cls,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        rules: SkillMatchingRules,
    ) -> Sequence[SkillMatchCandidate]:
        """Construct candidate pairs from resume and job skill features.

        Args:
            resume_features: Sequence of Resume Feature objects.
            job_features: Sequence of Job Description Feature objects.
            rules: Governing SkillMatchingRules configuration.

        Returns:
            A sequence of constructed SkillMatchCandidate instances.
        """
        if not rules.enabled:
            return []

        # Filter categories
        res_skills = [f for f in resume_features if f.category == FeatureCategory.SKILL]
        job_skills = [f for f in job_features if f.category == FeatureCategory.SKILL]

        candidates: list[SkillMatchCandidate] = []
        for r_feat in res_skills:
            for j_feat in job_skills:
                candidates.append(
                    SkillMatchCandidate(
                        resume_feature=r_feat,
                        job_feature=j_feat,
                    )
                )

        return candidates
