"""Certification extraction pipeline.

Purpose:
    Coordinate candidate building, validation, normalization, assembly,
    and entity building stages for certification extraction.
"""

from __future__ import annotations

import time

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.certification.certification_assembler import CertificationAssembler
from ats_engine.domain.entity_extraction.certification.certification_candidate_builder import CertificationCandidateBuilder
from ats_engine.domain.entity_extraction.certification.certification_candidate_validator import CertificationCandidateValidator
from ats_engine.domain.entity_extraction.certification.certification_entity_builder import CertificationEntityBuilder
from ats_engine.domain.entity_extraction.certification.certification_models import (
    CertificationCollection,
    CertificationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.certification.certification_normalizer import CertificationNormalizer
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class CertificationExtractionPipeline:
    """Stateless pipeline executing the full certification extraction sequence."""

    @classmethod
    def execute(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: CertificationExtractionRules,
    ) -> CertificationCollection:
        """Execute builder -> validator -> normalizer -> assembler -> entity builder pipeline.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            The compiled CertificationCollection DTO.
        """
        start_time = time.perf_counter()

        # 1. Candidate builder scan
        candidates = CertificationCandidateBuilder.build_candidates(document, sections, rules)

        # 2. Candidate validator check
        validated = [
            cand for cand in candidates
            if CertificationCandidateValidator.validate(cand, rules)
        ]

        # 3. Normalize validated candidates
        normalized = [CertificationNormalizer.normalize(cand, rules) for cand in validated]

        # 4. Assemble compound records
        assembled = CertificationAssembler.assemble(normalized, rules)

        # 5. Build final entities with confidence
        entities = [CertificationEntityBuilder.build(a, rules) for a in assembled]

        duration = time.perf_counter() - start_time

        # Compute active count representation (always active raw initially)
        stats = CertificationExtractionStatistics(
            total_certifications=len(entities),
            active_certifications=len(entities),
            execution_duration_seconds=duration,
        )

        return CertificationCollection(
            entities=tuple(entities),
            statistics=stats,
        )
