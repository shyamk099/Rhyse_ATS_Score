"""Skill normalizer transforming candidates to canonical forms.

Purpose:
    Expose normalization mappings that preserve matching provenance (direct name, alias, synonym).
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.skills.exceptions import SkillNormalizationError
from ats_engine.domain.entity_extraction.skills.skill_models import NormalizedSkill, SkillCandidate
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class SkillNormalizer:
    """Stateless normalizer wrapping candidate details with catalog definitions and categories."""

    @classmethod
    def normalize(cls, candidate: SkillCandidate, rules: SkillExtractionRules) -> NormalizedSkill:
        """Resolve canonical taxonomy attributes and create NormalizedSkill metadata.

        Args:
            candidate: Validated SkillCandidate.
            rules: The rules parameter mapping patterns.

        Returns:
            The NormalizedSkill metadata container.

        Raises:
            SkillNormalizationError: If candidate cannot be found in dictionary mapping.
        """
        defn = rules.dictionary.get(candidate.skill_id)
        if not defn:
            raise SkillNormalizationError(
                f"Candidate skill_id '{candidate.skill_id}' is missing from active dictionary."
            )

        alias = candidate.match_term if candidate.match_type == "alias" else None
        synonym = candidate.match_term if candidate.match_type == "synonym" else None

        return NormalizedSkill(
            candidate=candidate,
            skill_id=candidate.skill_id,
            canonical_name=defn.name,
            category=defn.category,
            matched_token=candidate.matched_text,
            normalized_token=defn.name,
            dictionary_entry=defn.name,
            alias_matched=alias,
            synonym_matched=synonym,
        )
