"""Contact information extractor implementation.

Purpose:
    Implement the generic EntityExtractor interface to parse phone, email, and links.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.entity_extraction.contact.candidate_validator import CandidateValidator
from ats_engine.domain.entity_extraction.contact.contact_rules import ContactExtractionRules
from ats_engine.domain.entity_extraction.contact.entity_builder import ContactEntityBuilder
from ats_engine.domain.entity_extraction.contact.normalizer import ContactNormalizer
from ats_engine.domain.entity_extraction.contact.pattern_candidate_builder import PatternCandidateBuilder
from ats_engine.domain.entity_extraction.extractor import EntityExtractor
from ats_engine.domain.entity_extraction.models import EntityExtractionContext, ExtractedEntity


class ContactInformationExtractor(EntityExtractor):
    """Stateless contact extractor executing Candidate -> Validator -> Normalizer -> Builder sequence."""

    def extract(
        self, segment: DocumentSegment, context: EntityExtractionContext
    ) -> Sequence[ExtractedEntity]:
        """Extract deterministic contact entities from a document segment text.

        Args:
            segment: The target DocumentSegment containing text content.
            context: Read-only context config mappings.

        Returns:
            A list of validated, normalized ExtractedEntity containers.
        """
        # Resolve config rules from context or default
        rules_payload = context.rule_engine_config.get("contact_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = ContactExtractionRules(**rules_payload)
        else:
            rules = ContactExtractionRules()

        # 1. Discover pattern candidates from segment text
        candidates = PatternCandidateBuilder.find_candidates(segment.text_content, rules)

        entities: list[ExtractedEntity] = []

        for candidate in candidates:
            # 2. Validate candidate structure
            if not CandidateValidator.validate_candidate(candidate):
                continue

            # 3. Clean value formatting
            normalized_value = ContactNormalizer.normalize(
                candidate.value, candidate.entity_type
            )

            # 4. Wrap into final domain ExtractedEntity
            entity = ContactEntityBuilder.build(
                candidate, normalized_value, segment.segment_id, rules
            )
            entities.append(entity)

        return entities
