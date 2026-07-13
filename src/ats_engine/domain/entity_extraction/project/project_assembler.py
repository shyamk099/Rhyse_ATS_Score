"""Project assembler.

Purpose:
    Group normalized project evidence into compound AssembledProject records.
    Resolves project technologies to canonical Skill IDs. Never fabricates.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.entity_extraction.project.project_models import (
    AssembledProject,
    NormalizedProject,
    ProjectTechnology,
)
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules


class ProjectAssembler:
    """Stateless assembler grouping evidence and assigning canonical project IDs."""

    @classmethod
    def assemble(
        cls,
        normalized_list: Sequence[NormalizedProject],
        rules: ProjectExtractionRules,
    ) -> Sequence[AssembledProject]:
        """Group normalized project candidates into compound records.

        Args:
            normalized_list: Pre-validated normalized project instances.
            rules: Configured extraction rules.

        Returns:
            A sequence of AssembledProject records.
        """
        assembled: list[AssembledProject] = []

        for idx, norm in enumerate(normalized_list, start=1):
            project_id = f"PROJ-{idx:08d}"

            # Extract structured lists
            techs = cls._extract_technologies(norm.candidate.raw_text, rules)
            resp, achs = cls._extract_lists(norm.candidate.raw_text)

            # Description is the overall text minus the list elements
            desc = cls._extract_description(norm.candidate.raw_text)

            assembled.append(
                AssembledProject(
                    project_id=project_id,
                    project_name=norm.project_name,
                    organization=norm.organization,
                    role=norm.role,
                    start_date_raw=norm.start_date_raw,
                    end_date_raw=norm.end_date_raw,
                    duration_raw=None,
                    technologies=tuple(techs),
                    responsibilities=tuple(resp),
                    achievements=tuple(achs),
                    project_description=desc,
                    repo_url=norm.repo_url,
                    demo_url=norm.demo_url,
                    location_raw=None,
                    source_segment_ids=(norm.candidate.segment_id,),
                    source_text=norm.candidate.raw_text,
                )
            )

        return assembled

    @classmethod
    def _extract_technologies(
        cls, raw_text: str, rules: ProjectExtractionRules
    ) -> list[ProjectTechnology]:
        """Extract technologies mentioned in project text using rules and resolve Skill IDs."""
        techs: list[ProjectTechnology] = []
        text_lower = raw_text.lower()

        for indicator in rules.technology_indicators:
            pattern = re.compile(rf"\b{indicator}\b", re.IGNORECASE)
            if pattern.search(text_lower):
                raw_name = indicator.replace("\\", "")
                
                # Check for canonical Skill ID mapping
                skill_id = rules.technology_skill_mappings.get(raw_name.lower())
                
                techs.append(
                    ProjectTechnology(
                        raw_name=raw_name,
                        skill_id=skill_id,
                    )
                )
        return techs

    @classmethod
    def _extract_lists(cls, raw_text: str) -> tuple[list[str], list[str]]:
        """Separate list entries into responsibilities and achievements."""
        responsibilities: list[str] = []
        achievements: list[str] = []
        lines = raw_text.split("\n")

        achievement_keywords = ("achieved", "increased", "reduced", "optimized", "improved", "saved", "won")

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith(("-", "•", "▪", "*", "–")):
                clean = stripped.lstrip("-•▪*– ").strip()
                if not clean:
                    continue

                clean_lower = clean.lower()
                if any(kw in clean_lower for kw in achievement_keywords) and any(c.isdigit() for c in clean):
                    achievements.append(clean)
                else:
                    responsibilities.append(clean)

        return responsibilities, achievements

    @classmethod
    def _extract_description(cls, raw_text: str) -> str | None:
        """Extract project description from text (excluding bullet points)."""
        lines = raw_text.split("\n")
        desc_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if not stripped.startswith(("-", "•", "▪", "*", "–")):
                desc_lines.append(stripped)
        
        if len(desc_lines) > 1:
            desc_text = " ".join(desc_lines[1:]).strip()
            return desc_text if desc_text else None
        
        return None
