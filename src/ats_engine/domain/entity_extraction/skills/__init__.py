"""Skill Extraction module.

Purpose:
    Expose pipeline managers, rules, exception structures, and builders for
    resolving resume and JD skill details.
"""

from ats_engine.domain.entity_extraction.skills.exceptions import (
    MatcherConfigurationError,
    SkillBuilderError,
    SkillCandidateValidationError,
    SkillExtractionError,
    SkillNormalizationError,
)
from ats_engine.domain.entity_extraction.skills.matcher import DictionaryMatcher, SkillMatcher
from ats_engine.domain.entity_extraction.skills.pipeline import SkillExtractionPipeline
from ats_engine.domain.entity_extraction.skills.skill_candidate_builder import SkillCandidateBuilder
from ats_engine.domain.entity_extraction.skills.skill_candidate_validator import SkillCandidateValidator
from ats_engine.domain.entity_extraction.skills.skill_entity_builder import SkillEntityBuilder
from ats_engine.domain.entity_extraction.skills.skill_models import (
    NormalizedSkill,
    SkillCandidate,
    SkillCollection,
    SkillExtractionStatistics,
)
from ats_engine.domain.entity_extraction.skills.skill_normalizer import SkillNormalizer
from ats_engine.domain.entity_extraction.skills.skill_rules import (
    SkillDefinition,
    SkillExtractionRules,
)
from ats_engine.domain.entity_extraction.skills.service import SkillExtractionService

__all__ = [
    "MatcherConfigurationError",
    "SkillBuilderError",
    "SkillCandidateValidationError",
    "SkillExtractionError",
    "SkillNormalizationError",
    "SkillMatcher",
    "DictionaryMatcher",
    "SkillExtractionPipeline",
    "SkillCandidateBuilder",
    "SkillCandidateValidator",
    "SkillEntityBuilder",
    "NormalizedSkill",
    "SkillCandidate",
    "SkillCollection",
    "SkillExtractionStatistics",
    "SkillNormalizer",
    "SkillDefinition",
    "SkillExtractionRules",
    "SkillExtractionService",
]
