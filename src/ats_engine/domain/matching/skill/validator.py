"""Structural validator for Skill matching candidates.

Purpose:
    Perform read-only checks asserting required identifier fields and correct
    feature categories without modifying features.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.feature_engineering.models import FeatureCategory
from ats_engine.domain.matching.skill.candidate_builder import SkillMatchCandidate
from ats_engine.domain.matching.skill.rules import SkillMatchingRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SkillMatchValidator:
    """Validator performing structural schema checks on SkillMatchCandidate objects."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(
        self,
        candidate: SkillMatchCandidate,
        rules: SkillMatchingRules,
    ) -> list[str]:
        """Validate candidate fields, categories, and identifier structures.

        Args:
            candidate: Candidate pair under evaluation.
            rules: Active SkillMatchingRules.

        Returns:
            A list of validation error/warning messages.
        """
        errors: list[str] = []

        rf = candidate.resume_feature
        jf = candidate.job_feature

        # 1. Feature Category checks
        if rf.category != FeatureCategory.SKILL:
            errors.append(f"Resume feature {rf.feature_id} category is not SKILL.")
        if jf.category != FeatureCategory.SKILL:
            errors.append(f"Job feature {jf.feature_id} category is not SKILL.")

        # 2. Empty ID checks
        if not rf.feature_id or not rf.feature_id.strip():
            errors.append("Resume skill feature is missing feature_id.")
        if not jf.feature_id or not jf.feature_id.strip():
            errors.append("Job skill feature is missing feature_id.")

        return errors
