"""Skill candidate builder orchestration.

Purpose:
    Expose candidate scanning coordinated by scope rules and matchers.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.domain.entity_extraction.skills.matcher import DictionaryMatcher, SkillMatcher
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCandidate
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class SkillCandidateBuilder:
    """Orchestrator driving skill matching over scoped sections and document segments."""

    def __init__(self, matcher: SkillMatcher | None = None) -> None:
        """Initialize builder with a matcher strategy."""
        self._matcher = matcher or DictionaryMatcher()

    def build_candidates(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: SkillExtractionRules,
    ) -> Sequence[SkillCandidate]:
        """Scan sections allowed by scope config and construct candidates.

        Args:
            document: Canonical document reference.
            sections: Detected logical sections.
            rules: Configured extraction scope rules.

        Returns:
            A sequence of discovered SkillCandidates.
        """
        candidates: list[SkillCandidate] = []
        scope = [s.upper() for s in rules.extraction_scope]
        scan_all = "ALL" in scope or not scope

        for section in sections.sections:
            stype = section.section_type.upper()
            if not scan_all and stype not in scope:
                continue

            for segment in section.associated_segments:
                segment_candidates = self._matcher.match(segment, rules, section.section_type)
                candidates.extend(segment_candidates)

        return candidates
