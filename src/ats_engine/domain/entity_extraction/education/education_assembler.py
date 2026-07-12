"""Education assembler.

Purpose:
    Group normalized education evidence into compound AssembledEducation records.
    Assigns canonical education IDs (EDU-XXXXXXXX).
    Never fabricates missing fields.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.entity_extraction.education.education_models import (
    AssembledEducation,
    NormalizedEducation,
)
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules


class EducationAssembler:
    """Stateless assembler grouping evidence and assigning canonical education IDs."""

    @classmethod
    def assemble(
        cls,
        normalized_list: Sequence[NormalizedEducation],
        rules: EducationExtractionRules,
    ) -> Sequence[AssembledEducation]:
        """Group normalized education candidates into compound records.

        Each validated candidate with a degree or institution becomes
        an independent education record.

        Args:
            normalized_list: Pre-validated normalized education instances.
            rules: Configured extraction rules.

        Returns:
            A sequence of AssembledEducation records.
        """
        assembled: list[AssembledEducation] = []

        for idx, norm in enumerate(normalized_list, start=1):
            education_id = f"EDU-{idx:08d}"

            # Extract structured collections
            honors = cls._extract_honors(norm.candidate.raw_text, rules)
            certifications = cls._extract_certifications(norm.candidate.raw_text)

            assembled.append(
                AssembledEducation(
                    education_id=education_id,
                    institution_name=norm.institution_name,
                    degree=norm.degree,
                    specialization=norm.specialization,
                    field_of_study=norm.field_of_study,
                    start_date_raw=norm.start_date_raw,
                    end_date_raw=norm.end_date_raw,
                    graduation_date_raw=norm.graduation_date_raw,
                    gpa_raw=norm.gpa_raw,
                    grade_raw=norm.grade_raw,
                    honors=tuple(honors),
                    certifications=tuple(certifications),
                    location_raw=None,
                    source_segment_ids=(norm.candidate.segment_id,),
                    source_text=norm.candidate.raw_text,
                )
            )

        return assembled

    @classmethod
    def _extract_honors(
        cls, raw_text: str, rules: EducationExtractionRules
    ) -> list[str]:
        """Extract honors/distinction mentions from raw text.

        Preserves ordering. Does NOT fabricate entries.
        """
        honors: list[str] = []
        text_lower = raw_text.lower()

        for indicator in rules.honors_indicators:
            if indicator.lower() in text_lower:
                honors.append(indicator)

        return honors

    @classmethod
    def _extract_certifications(cls, raw_text: str) -> list[str]:
        """Extract certifications listed within education text.

        Detects bullet-pointed certification entries.
        Preserves ordering. Does NOT fabricate entries.
        """
        certifications: list[str] = []
        lines = raw_text.split("\n")

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("-", "•", "▪", "*", "–")):
                clean = stripped.lstrip("-•▪*– ").strip()
                if clean and any(
                    kw in clean.lower()
                    for kw in ("certified", "certification", "certificate", "license", "licensed")
                ):
                    certifications.append(clean)

        return certifications
