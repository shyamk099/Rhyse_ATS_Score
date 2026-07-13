"""Project Extraction module.

Purpose:
    Expose services, rules, models, exception hierarchy, and pipeline
    components for compound project entity extraction.
"""

from ats_engine.domain.entity_extraction.project.exceptions import (
    ProjectAssemblyError,
    ProjectBuilderError,
    ProjectCandidateValidationError,
    ProjectExtractionError,
    ProjectNormalizationError,
)
from ats_engine.domain.entity_extraction.project.project_assembler import ProjectAssembler
from ats_engine.domain.entity_extraction.project.project_candidate_builder import ProjectCandidateBuilder
from ats_engine.domain.entity_extraction.project.project_candidate_validator import ProjectCandidateValidator
from ats_engine.domain.entity_extraction.project.project_entity_builder import ProjectEntityBuilder
from ats_engine.domain.entity_extraction.project.project_models import (
    AssembledProject,
    ProjectCandidate,
    ProjectCollection,
    ProjectEntity,
    ProjectExtractionStatistics,
    NormalizedProject,
    ProjectTechnology,
    ProjectURL,
)
from ats_engine.domain.entity_extraction.project.project_normalizer import ProjectNormalizer
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.project.pipeline import ProjectExtractionPipeline
from ats_engine.domain.entity_extraction.project.service import ProjectExtractionService

__all__ = [
    "ProjectAssemblyError",
    "ProjectBuilderError",
    "ProjectCandidateValidationError",
    "ProjectExtractionError",
    "ProjectNormalizationError",
    "ProjectAssembler",
    "ProjectCandidateBuilder",
    "ProjectCandidateValidator",
    "ProjectEntityBuilder",
    "AssembledProject",
    "ProjectCandidate",
    "ProjectCollection",
    "ProjectEntity",
    "ProjectExtractionStatistics",
    "NormalizedProject",
    "ProjectTechnology",
    "ProjectURL",
    "ProjectNormalizer",
    "ProjectExtractionRules",
    "ProjectExtractionPipeline",
    "ProjectExtractionService",
]
