"""Skill extraction pipeline coordinating scanning, validation, normalization, and filters.

Purpose:
    Expose the execution pipeline to map raw segments into structured, unique skill entities.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.domain.entity_extraction.skills.duplicate_resolver import DuplicateResolver
from ats_engine.domain.entity_extraction.skills.skill_candidate_builder import SkillCandidateBuilder
from ats_engine.domain.entity_extraction.skills.skill_candidate_validator import SkillCandidateValidator
from ats_engine.domain.entity_extraction.skills.skill_entity_builder import SkillEntityBuilder
from ats_engine.domain.entity_extraction.skills.skill_models import (
    SkillCollection,
    SkillExtractionStatistics,
)
from ats_engine.domain.entity_extraction.skills.skill_normalizer import SkillNormalizer
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class SkillExtractionPipeline:
    """Orchestrator pipeline resolving dictionary matches, duplicates, and normalizations."""

    def __init__(self, builder: SkillCandidateBuilder | None = None) -> None:
        """Initialize pipeline with builder dependency."""
        self._builder = builder or SkillCandidateBuilder()

    def execute(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: SkillExtractionRules,
    ) -> SkillCollection:
        """Execute the builder -> validator -> normalizer -> resolver -> builder pipeline.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: The rules parameter mapping patterns.

        Returns:
            The compiled, resolved SkillCollection DTO.
        """
        start_time = time.perf_counter()

        # 1. Candidate builder scan
        candidates = self._builder.build_candidates(document, sections, rules)

        # 2. Candidate validator check
        validated = [
            cand for cand in candidates if SkillCandidateValidator.validate(cand, rules)
        ]

        # 3. Candidate normalizer transformation
        normalized = [SkillNormalizer.normalize(cand, rules) for cand in validated]

        # 4. Duplicate resolver filtering (BEFORE entity building)
        resolved = DuplicateResolver.resolve(normalized, rules)

        # 5. Domain ExtractedEntity building
        entities = [SkillEntityBuilder.build(ns, rules) for ns in resolved]

        duration = time.perf_counter() - start_time

        unique_count = len({entity.value for entity in entities})
        stats = SkillExtractionStatistics(
            total_skills_found=len(entities),
            unique_skills_count=unique_count,
            execution_duration_seconds=duration,
        )

        return SkillCollection(
            entities=tuple(entities),
            statistics=stats,
        )
