"""Education extraction pipeline.

Purpose:
    Coordinate candidate building, validation, normalization, assembly,
    and entity building stages for education extraction.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.education.education_assembler import EducationAssembler
from ats_engine.domain.entity_extraction.education.education_candidate_builder import EducationCandidateBuilder
from ats_engine.domain.entity_extraction.education.education_candidate_validator import EducationCandidateValidator
from ats_engine.domain.entity_extraction.education.education_entity_builder import EducationEntityBuilder
from ats_engine.domain.entity_extraction.education.education_models import (
    EducationCollection,
    EducationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.education.education_normalizer import EducationNormalizer
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class EducationExtractionPipeline:
    """Stateless pipeline executing the full education extraction sequence."""

    @classmethod
    def execute(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: EducationExtractionRules,
    ) -> EducationCollection:
        """Execute builder -> validator -> normalizer -> assembler -> entity builder pipeline.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            The compiled EducationCollection DTO.
        """
        start_time = time.perf_counter()

        # 1. Candidate builder scan
        candidates = EducationCandidateBuilder.build_candidates(document, sections, rules)

        # 2. Candidate validator check
        validated = [
            cand for cand in candidates
            if EducationCandidateValidator.validate(cand, rules)
        ]

        # 3. Normalize validated candidates
        normalized = [EducationNormalizer.normalize(cand, rules) for cand in validated]

        # 4. Assemble compound records
        assembled = EducationAssembler.assemble(normalized, rules)

        # 5. Build final entities with confidence
        entities = [EducationEntityBuilder.build(a, rules) for a in assembled]

        duration = time.perf_counter() - start_time

        degree_count = sum(1 for e in entities if e.degree)
        gpa_count = sum(1 for e in entities if e.gpa_raw)
        stats = EducationExtractionStatistics(
            total_education_records=len(entities),
            records_with_degree=degree_count,
            records_with_gpa=gpa_count,
            execution_duration_seconds=duration,
        )

        return EducationCollection(
            entities=tuple(entities),
            statistics=stats,
        )
