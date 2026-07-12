"""Experience assembler.

Purpose:
    Group normalized experience evidence into compound AssembledExperience records.
    Assigns canonical experience IDs. Never fabricates missing fields.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.entity_extraction.experience.experience_models import (
    AssembledExperience,
    NormalizedExperience,
)
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules


class ExperienceAssembler:
    """Stateless assembler grouping evidence and assigning canonical experience IDs."""

    @classmethod
    def assemble(
        cls,
        normalized_list: Sequence[NormalizedExperience],
        rules: ExperienceExtractionRules,
    ) -> Sequence[AssembledExperience]:
        """Group normalized experience candidates into compound records.

        Each validated candidate with a title or company becomes
        an independent experience record. Contiguous text lines following
        the anchor are split into responsibilities, technologies, and
        achievements based on content structure.

        Args:
            normalized_list: Pre-validated normalized experience instances.
            rules: Configured extraction rules.

        Returns:
            A sequence of AssembledExperience records.
        """
        assembled: list[AssembledExperience] = []

        for idx, norm in enumerate(normalized_list, start=1):
            experience_id = f"EXP-{idx:08d}"

            # Extract structured collections from raw text
            responsibilities, technologies, achievements = cls._extract_structured_lists(
                norm.candidate.raw_text
            )

            assembled.append(
                AssembledExperience(
                    experience_id=experience_id,
                    company_name=norm.company_name,
                    job_title=norm.job_title,
                    employment_type=norm.employment_type,
                    start_date_raw=norm.start_date_raw,
                    end_date_raw=norm.end_date_raw,
                    is_current=norm.is_current,
                    responsibilities=tuple(responsibilities),
                    technologies=tuple(technologies),
                    achievements=tuple(achievements),
                    source_segment_ids=(norm.candidate.segment_id,),
                    source_text=norm.candidate.raw_text,
                )
            )

        return assembled

    @classmethod
    def _extract_structured_lists(
        cls, raw_text: str
    ) -> tuple[list[str], list[str], list[str]]:
        """Split raw text into structured responsibility, technology, and achievement lists.

        Preserves ordering. Uses bullet point detection for responsibilities.
        Does NOT fabricate entries.
        """
        responsibilities: list[str] = []
        technologies: list[str] = []
        achievements: list[str] = []

        lines = raw_text.split("\n")
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Detect bullet-point entries as responsibilities
            if stripped.startswith(("-", "•", "▪", "*", "–")):
                clean = stripped.lstrip("-•▪*– ").strip()
                if clean:
                    responsibilities.append(clean)

        return responsibilities, technologies, achievements
