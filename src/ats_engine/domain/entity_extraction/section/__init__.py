"""Document Section Detection module.

Purpose:
    Expose services, rules, pipelines, exception hierarchies, and models for
    parsing logical document sections.
"""

from ats_engine.domain.entity_extraction.section.exceptions import (
    BoundaryResolutionError,
    HeadingValidationError,
    SectionBuilderError,
    SectionDetectionError,
)
from ats_engine.domain.entity_extraction.section.heading_validator import HeadingValidator
from ats_engine.domain.entity_extraction.section.pipeline import SectionDetectionPipeline
from ats_engine.domain.entity_extraction.section.section_boundary_resolver import (
    SectionBoundary,
    SectionBoundaryResolver,
)
from ats_engine.domain.entity_extraction.section.section_builder import SectionBuilder
from ats_engine.domain.entity_extraction.section.section_candidate_builder import SectionCandidateBuilder
from ats_engine.domain.entity_extraction.section.section_models import (
    Section,
    SectionCandidate,
    SectionCollection,
    SectionDetectionStatistics,
    SectionMetadata,
)
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules
from ats_engine.domain.entity_extraction.section.service import SectionDetectionService

__all__ = [
    "BoundaryResolutionError",
    "HeadingValidationError",
    "SectionBuilderError",
    "SectionDetectionError",
    "HeadingValidator",
    "SectionDetectionPipeline",
    "SectionBoundary",
    "SectionBoundaryResolver",
    "SectionBuilder",
    "SectionCandidateBuilder",
    "Section",
    "SectionCandidate",
    "SectionCollection",
    "SectionDetectionStatistics",
    "SectionMetadata",
    "SectionDetectionRules",
    "SectionDetectionService",
]
