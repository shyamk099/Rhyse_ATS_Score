"""Experience extraction pipeline.

Purpose:
    Coordinate candidate building, validation, normalization, assembly,
    and entity building stages.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.experience.experience_assembler import ExperienceAssembler
from ats_engine.domain.entity_extraction.experience.experience_candidate_builder import ExperienceCandidateBuilder
from ats_engine.domain.entity_extraction.experience.experience_candidate_validator import ExperienceCandidateValidator
from ats_engine.domain.entity_extraction.experience.experience_entity_builder import ExperienceEntityBuilder
from ats_engine.domain.entity_extraction.experience.experience_models import (
    ExperienceCollection,
    ExperienceExtractionStatistics,
)
from ats_engine.domain.entity_extraction.experience.experience_normalizer import ExperienceNormalizer
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class ExperienceExtractionPipeline:
    """Stateless pipeline executing the full experience extraction sequence."""

    @classmethod
    def execute(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: ExperienceExtractionRules,
    ) -> ExperienceCollection:
        """Execute builder -> validator -> normalizer -> assembler -> entity builder pipeline.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            The compiled ExperienceCollection DTO.
        """
        start_time = time.perf_counter()

        # 1. Candidate builder scan
        candidates = ExperienceCandidateBuilder.build_candidates(document, sections, rules)

        # 2. Candidate validator check
        validated = [
            cand for cand in candidates
            if ExperienceCandidateValidator.validate(cand, rules)
        ]

        # 3. Normalize validated candidates
        normalized = [ExperienceNormalizer.normalize(cand, rules) for cand in validated]

        # 4. Assemble compound records
        assembled = ExperienceAssembler.assemble(normalized, rules)

        # 5. Build final entities with confidence
        entities = [ExperienceEntityBuilder.build(a, rules) for a in assembled]

        duration = time.perf_counter() - start_time

        current_count = sum(1 for e in entities if e.is_current)
        stats = ExperienceExtractionStatistics(
            total_experiences=len(entities),
            current_employment_count=current_count,
            execution_duration_seconds=duration,
        )

        return ExperienceCollection(
            entities=tuple(entities),
            statistics=stats,
        )
