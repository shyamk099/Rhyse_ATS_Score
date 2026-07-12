"""Contact Information Extraction module.

Purpose:
    Expose extractors, rules, exception structures, and builders for contact details parsing.
"""

from ats_engine.domain.entity_extraction.contact.candidate_validator import CandidateValidator
from ats_engine.domain.entity_extraction.contact.contact_rules import ContactExtractionRules
from ats_engine.domain.entity_extraction.contact.entity_builder import ContactEntityBuilder
from ats_engine.domain.entity_extraction.contact.exceptions import (
    CandidateValidationError,
    ContactExtractionError,
    NormalizationError,
    PatternConfigurationError,
)
from ats_engine.domain.entity_extraction.contact.extractor import ContactInformationExtractor
from ats_engine.domain.entity_extraction.contact.normalizer import ContactNormalizer
from ats_engine.domain.entity_extraction.contact.pattern_candidate_builder import PatternCandidateBuilder

__all__ = [
    "CandidateValidator",
    "ContactExtractionRules",
    "ContactEntityBuilder",
    "CandidateValidationError",
    "ContactExtractionError",
    "NormalizationError",
    "PatternConfigurationError",
    "ContactInformationExtractor",
    "ContactNormalizer",
    "PatternCandidateBuilder",
]
