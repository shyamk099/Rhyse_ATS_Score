"""Experience matching module initialization.

Purpose:
    Expose concrete Experience matching classes and configurations.
"""

from __future__ import annotations

from ats_engine.domain.matching.experience.builder import ExperienceMatchBuilder
from ats_engine.domain.matching.experience.candidate_builder import (
    ExperienceMatchCandidate,
    ExperienceMatchCandidateBuilder,
)
from ats_engine.domain.matching.experience.matcher import ExperienceMatcher
from ats_engine.domain.matching.experience.normalizer import ExperienceMatchNormalizer
from ats_engine.domain.matching.experience.rules import ExperienceMatchingRules
from ats_engine.domain.matching.experience.validator import ExperienceMatchValidator

__all__ = [
    "ExperienceMatcher",
    "ExperienceMatchingRules",
    "ExperienceMatchCandidate",
    "ExperienceMatchCandidateBuilder",
    "ExperienceMatchValidator",
    "ExperienceMatchNormalizer",
    "ExperienceMatchBuilder",
]
