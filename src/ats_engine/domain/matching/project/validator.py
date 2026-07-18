"""Structural validator for Project matching candidates.

Purpose:
    Perform read-only checks asserting required identifier fields and correct
    feature categories without modifying features.
"""

from __future__ import annotations

import logging

from ats_engine.domain.feature_engineering.models import FeatureCategory
from ats_engine.domain.matching.project.candidate_builder import ProjectMatchCandidate
from ats_engine.domain.matching.project.rules import ProjectMatchingRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ProjectMatchValidator:
    """Validator performing structural schema checks on ProjectMatchCandidate objects."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(
        self,
        candidate: ProjectMatchCandidate,
        rules: ProjectMatchingRules,
    ) -> list[str]:
        """Validate candidate fields, categories, and identifier structures."""
        errors: list[str] = []

        rf = candidate.resume_feature
        jf = candidate.job_feature

        if rf.category != FeatureCategory.PROJECT:
            errors.append(f"Resume feature {rf.feature_id} category is not PROJECT.")
        if jf.category != FeatureCategory.PROJECT:
            errors.append(f"Job feature {jf.feature_id} category is not PROJECT.")

        if not rf.feature_id or not rf.feature_id.strip():
            errors.append("Resume project feature is missing feature_id.")
        if not jf.feature_id or not jf.feature_id.strip():
            errors.append("Job project feature is missing feature_id.")

        return errors
