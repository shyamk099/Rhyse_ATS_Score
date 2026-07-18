"""Candidate pair builder for Project features.

Purpose:
    Filter input features down to FeatureCategory.PROJECT, filter out empty records,
    and pair them into ProjectMatchCandidate structures.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict

from ats_engine.domain.feature_engineering.models import Feature, FeatureCategory
from ats_engine.domain.matching.project.rules import ProjectMatchingRules


class ProjectMatchCandidate(BaseModel):
    """Immutable model representing a candidate resume-job project pair for matching evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    resume_feature: Feature
    job_feature: Feature


class ProjectMatchCandidateBuilder:
    """Builder constructing candidate pairs restricted strictly to Project features."""

    @classmethod
    def _is_empty_project(cls, feature: Feature) -> bool:
        """Check if all matching fields (project_name, organization, role) are None or empty."""
        val = feature.value or {}
        name = val.get("project_name")
        org = val.get("organization")
        role = val.get("role")

        return not any(
            str(x).strip() for x in [name, org, role] if x is not None
        )

    @classmethod
    def build_candidates(
        cls,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        rules: ProjectMatchingRules,
    ) -> Sequence[ProjectMatchCandidate]:
        """Construct candidate pairs from resume and job project features.

        Args:
            resume_features: Sequence of Resume Feature objects.
            job_features: Sequence of Job Description Feature objects.
            rules: Governing ProjectMatchingRules configuration.

        Returns:
            A sequence of constructed ProjectMatchCandidate instances.
        """
        if not rules.enabled:
            return []

        res_proj = [f for f in resume_features if f.category == FeatureCategory.PROJECT]
        job_proj = [f for f in job_features if f.category == FeatureCategory.PROJECT]

        candidates: list[ProjectMatchCandidate] = []
        for r_feat in res_proj:
            if cls._is_empty_project(r_feat):
                continue
            for j_feat in job_proj:
                if cls._is_empty_project(j_feat):
                    continue
                candidates.append(
                    ProjectMatchCandidate(
                        resume_feature=r_feat,
                        job_feature=j_feat,
                    )
                )

        return candidates
