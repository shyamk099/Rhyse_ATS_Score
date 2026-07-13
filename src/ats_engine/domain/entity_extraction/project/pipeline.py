"""Project extraction pipeline.

Purpose:
    Coordinate candidate building, validation, normalization, assembly,
    and entity building stages for project extraction.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.project.project_assembler import ProjectAssembler
from ats_engine.domain.entity_extraction.project.project_candidate_builder import ProjectCandidateBuilder
from ats_engine.domain.entity_extraction.project.project_candidate_validator import ProjectCandidateValidator
from ats_engine.domain.entity_extraction.project.project_entity_builder import ProjectEntityBuilder
from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectCollection,
    ProjectExtractionStatistics,
)
from ats_engine.domain.entity_extraction.project.project_normalizer import ProjectNormalizer
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class ProjectExtractionPipeline:
    """Stateless pipeline executing the full project extraction sequence."""

    @classmethod
    def execute(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: ProjectExtractionRules,
    ) -> ProjectCollection:
        """Execute builder -> validator -> normalizer -> assembler -> entity builder pipeline.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            The compiled ProjectCollection DTO.
        """
        start_time = time.perf_counter()

        # 1. Candidate builder scan
        candidates = ProjectCandidateBuilder.build_candidates(document, sections, rules)

        # 2. Candidate validator check
        validated = [
            cand for cand in candidates
            if ProjectCandidateValidator.validate(cand, rules)
        ]

        # 3. Normalize validated candidates
        normalized = [ProjectNormalizer.normalize(cand, rules) for cand in validated]

        # 4. Assemble compound records
        assembled = ProjectAssembler.assemble(normalized, rules)

        # 5. Build final entities with confidence
        entities = [ProjectEntityBuilder.build(a, rules) for a in assembled]

        duration = time.perf_counter() - start_time

        repo_count = sum(1 for e in entities if e.repo_url)
        demo_count = sum(1 for e in entities if e.demo_url)
        stats = ProjectExtractionStatistics(
            total_projects=len(entities),
            projects_with_repo=repo_count,
            projects_with_demo=demo_count,
            execution_duration_seconds=duration,
        )

        return ProjectCollection(
            entities=tuple(entities),
            statistics=stats,
        )
