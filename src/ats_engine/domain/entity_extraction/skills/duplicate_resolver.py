"""Duplicate and overlap resolver for extracted skills.

Purpose:
    Filter and resolve candidate skill overlaps (longest match wins) and duplicates
    (KEEP_FIRST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL) before entity building.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.entity_extraction.skills.skill_models import NormalizedSkill
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules


class DuplicateResolver:
    """Stateless processor resolving spans overlap conflicts and duplicate skill occurrences."""

    @classmethod
    def resolve(
        cls,
        normalized_skills: Sequence[NormalizedSkill],
        rules: SkillExtractionRules,
    ) -> Sequence[NormalizedSkill]:
        """Filter out overlaps and duplicates based on active strategy rules.

        Args:
            normalized_skills: Pre-validated normalized skill instances.
            rules: Configured extraction rules.

        Returns:
            A resolved sequence of NormalizedSkills.
        """
        if not normalized_skills:
            return []

        # 1. Resolve overlaps in character spans per segment (Longest Match Wins)
        non_overlapping = cls._resolve_overlaps(normalized_skills, rules)

        # 2. Resolve duplicate occurrences of the same skill across the document
        resolved = cls._resolve_duplicates(non_overlapping, rules)

        return resolved

    @classmethod
    def _resolve_overlaps(
        cls,
        skills: Sequence[NormalizedSkill],
        rules: SkillExtractionRules,
    ) -> Sequence[NormalizedSkill]:
        if rules.overlap_strategy != "LONGEST_MATCH":
            return skills

        # Group by segment
        by_segment: dict[str, list[NormalizedSkill]] = {}
        for ns in skills:
            by_segment.setdefault(ns.candidate.segment_id, []).append(ns)

        non_overlapping: list[NormalizedSkill] = []

        for seg_id, seg_skills in by_segment.items():
            # Sort by length of matched text descending (Longest Match Wins)
            sorted_skills = sorted(
                seg_skills, key=lambda ns: len(ns.matched_token), reverse=True
            )
            selected_spans: list[tuple[int, int]] = []

            for ns in sorted_skills:
                start = ns.candidate.start_char
                end = ns.candidate.end_char

                overlap = False
                for s_start, s_end in selected_spans:
                    if not (end <= s_start or start >= s_end):
                        overlap = True
                        break

                if not overlap:
                    selected_spans.append((start, end))
                    non_overlapping.append(ns)

        return non_overlapping

    @classmethod
    def _resolve_duplicates(
        cls,
        skills: Sequence[NormalizedSkill],
        rules: SkillExtractionRules,
    ) -> Sequence[NormalizedSkill]:
        strategy = rules.duplicate_strategy.upper()
        if strategy == "KEEP_ALL":
            return skills

        def get_confidence(ns: NormalizedSkill) -> float:
            stype = ns.candidate.section_type.upper()
            return rules.confidence_mappings.get(
                stype,
                rules.confidence_mappings.get("DEFAULT", rules.default_confidence),
            )

        # Group by skill_id
        by_skill: dict[str, list[NormalizedSkill]] = {}
        for ns in skills:
            by_skill.setdefault(ns.skill_id, []).append(ns)

        resolved: list[NormalizedSkill] = []

        for skill_id, skill_occurrences in by_skill.items():
            if strategy == "KEEP_FIRST":
                # Occurrences are already gathered in reading order since candidate scanning follows document sequence.
                # Keep first match.
                resolved.append(skill_occurrences[0])

            elif strategy == "KEEP_HIGHEST_CONFIDENCE":
                # Sort by confidence descending, keep highest
                sorted_occ = sorted(
                    skill_occurrences, key=lambda ns: get_confidence(ns), reverse=True
                )
                resolved.append(sorted_occ[0])
            else:
                resolved.extend(skill_occurrences)

        return resolved
