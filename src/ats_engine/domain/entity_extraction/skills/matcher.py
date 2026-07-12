"""Skill matching strategies and interfaces.

Purpose:
    Define a generic SkillMatcher protocol and a concrete DictionaryMatcher implementation.
"""

from __future__ import annotations

import re
from typing import Protocol, Sequence, runtime_checkable

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment
from ats_engine.domain.entity_extraction.skills.exceptions import MatcherConfigurationError
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCandidate
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


@runtime_checkable
class SkillMatcher(Protocol):
    """Protocol defining the interface for matching skill tokens within text segments."""

    def match(
        self,
        segment: DocumentSegment,
        rules: SkillExtractionRules,
        section_type: str,
    ) -> Sequence[SkillCandidate]:
        """Scan a segment and return discovered skill candidates.

        Args:
            segment: The DocumentSegment containing text.
            rules: Configured SkillExtractionRules.
            section_type: Logical section type containing this segment.
        """
        ...


class DictionaryMatcher:
    """Matcher performing word-boundary scans against configured dictionary, aliases, and synonyms."""

    def match(
        self,
        segment: DocumentSegment,
        rules: SkillExtractionRules,
        section_type: str,
    ) -> Sequence[SkillCandidate]:
        """Find matching terms using regular expressions.

        Args:
            segment: Target segment to scan.
            rules: Taxonomy and rule parameters.
            section_type: logical section type containing this segment.

        Returns:
            A sequence of populated SkillCandidates.

        Raises:
            MatcherConfigurationError: If compiling match regexes fails.
        """
        candidates: list[SkillCandidate] = []
        text = segment.text_content
        seg_id = segment.segment_id

        for skill_id, defn in rules.dictionary.items():
            # 1. Direct Name Match
            try:
                name_pat = re.compile(rf"\b{re.escape(defn.name)}\b", re.IGNORECASE)
            except re.error as error:
                raise MatcherConfigurationError(f"Bad regex for skill name '{defn.name}': {error}") from error

            for m in name_pat.finditer(text):
                candidates.append(
                    SkillCandidate(
                        matched_text=m.group(0),
                        start_char=m.start(),
                        end_char=m.end(),
                        skill_id=skill_id,
                        match_type="direct",
                        match_term=defn.name,
                        segment_id=seg_id,
                        section_type=section_type,
                    )
                )

            # 2. Aliases Match
            for alias in defn.aliases:
                try:
                    alias_pat = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
                except re.error as error:
                    raise MatcherConfigurationError(f"Bad regex for skill alias '{alias}': {error}") from error

                for m in alias_pat.finditer(text):
                    candidates.append(
                        SkillCandidate(
                            matched_text=m.group(0),
                            start_char=m.start(),
                            end_char=m.end(),
                            skill_id=skill_id,
                            match_type="alias",
                            match_term=alias,
                            segment_id=seg_id,
                            section_type=section_type,
                        )
                    )

            # 3. Synonyms Match
            for syn in defn.synonyms:
                try:
                    syn_pat = re.compile(rf"\b{re.escape(syn)}\b", re.IGNORECASE)
                except re.error as error:
                    raise MatcherConfigurationError(f"Bad regex for skill synonym '{syn}': {error}") from error

                for m in syn_pat.finditer(text):
                    candidates.append(
                        SkillCandidate(
                            matched_text=m.group(0),
                            start_char=m.start(),
                            end_char=m.end(),
                            skill_id=skill_id,
                            match_type="synonym",
                            match_term=syn,
                            segment_id=seg_id,
                            section_type=section_type,
                        )
                    )

        return candidates
