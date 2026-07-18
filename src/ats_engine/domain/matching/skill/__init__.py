"""Skill matching module initialization.

Purpose:
    Expose concrete Skill matching classes and configurations.
"""

from __future__ import annotations

from ats_engine.domain.matching.skill.builder import SkillMatchBuilder
from ats_engine.domain.matching.skill.candidate_builder import (
    SkillMatchCandidate,
    SkillMatchCandidateBuilder,
)
from ats_engine.domain.matching.skill.matcher import SkillMatcher
from ats_engine.domain.matching.skill.normalizer import SkillMatchNormalizer
from ats_engine.domain.matching.skill.rules import SkillMatchingRules
from ats_engine.domain.matching.skill.validator import SkillMatchValidator

__all__ = [
    "SkillMatcher",
    "SkillMatchingRules",
    "SkillMatchCandidate",
    "SkillMatchCandidateBuilder",
    "SkillMatchValidator",
    "SkillMatchNormalizer",
    "SkillMatchBuilder",
]
