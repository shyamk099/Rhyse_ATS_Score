"""Skill entity builder.

Purpose:
    Compile NormalizedSkill models into final Domain ExtractedEntities.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.models import EntityLocation, ExtractedEntity
from ats_engine.domain.entity_extraction.skills.skill_models import NormalizedSkill
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class SkillEntityBuilder:
    """Stateless builder converting NormalizedSkills into final domain ExtractedEntities."""

    @classmethod
    def build(cls, ns: NormalizedSkill, rules: SkillExtractionRules) -> ExtractedEntity:
        """Construct an ExtractedEntity with taxonomy metrics and confidence reasons.

        Args:
            ns: The NormalizedSkill carrying provenance.
            rules: Configured extraction rules.

        Returns:
            The compiled, immutable ExtractedEntity.
        """
        stype = ns.candidate.section_type.upper()
        confidence = rules.confidence_mappings.get(
            stype,
            rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
        )

        match_type = ns.candidate.match_type
        match_term = ns.candidate.match_term
        reason = (
            f"Matched skill ID '{ns.skill_id}' via {match_type} match "
            f"on term '{match_term}' in section '{stype}'. "
            f"Assigned confidence of {confidence} from rules."
        )

        metadata = {
            "matched_token": ns.matched_token,
            "normalized_token": ns.normalized_token,
            "dictionary_entry": ns.dictionary_entry,
            "alias_matched": ns.alias_matched or "",
            "synonym_matched": ns.synonym_matched or "",
            "category": ns.category,
            "skill_id": ns.skill_id,
            "confidence_reason": reason,
        }

        location = EntityLocation(
            segment_id=ns.candidate.segment_id,
            start_char=ns.candidate.start_char,
            end_char=ns.candidate.end_char,
        )

        return ExtractedEntity(
            entity_type="SKILL",
            value=ns.canonical_name,
            confidence=confidence,
            location=location,
            metadata=metadata,
        )
