"""Education matching module initialization.

Purpose:
    Expose concrete Education matching classes and configurations.
"""

from __future__ import annotations

from ats_engine.domain.matching.education.builder import EducationMatchBuilder
from ats_engine.domain.matching.education.candidate_builder import (
    EducationMatchCandidate,
    EducationMatchCandidateBuilder,
)
from ats_engine.domain.matching.education.matcher import EducationMatcher
from ats_engine.domain.matching.education.normalizer import EducationMatchNormalizer
from ats_engine.domain.matching.education.rules import EducationMatchingRules
from ats_engine.domain.matching.education.validator import EducationMatchValidator

__all__ = [
    "EducationMatcher",
    "EducationMatchingRules",
    "EducationMatchCandidate",
    "EducationMatchCandidateBuilder",
    "EducationMatchValidator",
    "EducationMatchNormalizer",
    "EducationMatchBuilder",
]
