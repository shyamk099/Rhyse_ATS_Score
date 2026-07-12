"""Education candidate builder.

Purpose:
    Scan permitted sections and segments for degree indicators, institution
    indicators, date ranges, GPA/CGPA patterns, grade patterns, and major
    indicators to build raw education candidates.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.education.education_models import EducationCandidate
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class EducationCandidateBuilder:
    """Stateless builder scanning segments for education evidence."""

    @classmethod
    def build_candidates(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: EducationExtractionRules,
    ) -> Sequence[EducationCandidate]:
        """Scan sections allowed by scope config and extract raw education candidates.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            A sequence of discovered EducationCandidates.
        """
        candidates: list[EducationCandidate] = []
        scope = [s.upper() for s in rules.extraction_scope]
        scan_all = "ALL" in scope or not scope

        # Compile date patterns
        date_patterns = [re.compile(p, re.IGNORECASE) for p in rules.date_patterns]
        graduation_indicators = [gi.lower() for gi in rules.graduation_indicators]

        for section in sections.sections:
            stype = section.section_type.upper()
            if not scan_all and stype not in scope:
                continue

            for segment in section.associated_segments:
                text = segment.text_content
                if not text.strip():
                    continue

                # Detect dates
                detected_dates: list[str] = []
                for pat in date_patterns:
                    for m in pat.finditer(text):
                        detected_dates.append(m.group(0))

                # Detect graduation indicator
                text_lower = text.lower()
                has_graduation = any(gi in text_lower for gi in graduation_indicators)

                # Detect institution via configurable indicators
                detected_institution = cls._detect_institution(text, rules)

                # Detect degree via configurable indicators
                detected_degree = cls._detect_degree(text, rules)

                # Detect major/specialization
                detected_major = cls._detect_major(text, rules)

                # Detect GPA/CGPA
                detected_gpa = cls._detect_gpa(text, rules)

                # Detect grade
                detected_grade = cls._detect_grade(text, rules)

                # Only create candidate if there's meaningful evidence
                if detected_institution or detected_degree or detected_gpa or detected_grade:
                    candidates.append(
                        EducationCandidate(
                            segment_id=segment.segment_id,
                            section_type=section.section_type,
                            raw_text=text,
                            start_char=0,
                            end_char=len(text),
                            detected_dates=tuple(detected_dates),
                            detected_institution=detected_institution,
                            detected_degree=detected_degree,
                            detected_major=detected_major,
                            detected_gpa=detected_gpa,
                            detected_grade=detected_grade,
                            has_graduation_indicator=has_graduation,
                        )
                    )

        return candidates

    @classmethod
    def _detect_institution(cls, text: str, rules: EducationExtractionRules) -> str | None:
        """Detect institution name using configurable institution indicators."""
        for indicator in rules.institution_indicators:
            pattern = re.compile(
                rf"([A-Z][A-Za-z0-9\s&.',-]*\b{re.escape(indicator)}\b[A-Za-z0-9\s&.',-]*)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                result = match.group(0).strip().rstrip(",.-")
                if len(result) > 3:
                    return result
        return None

    @classmethod
    def _detect_degree(cls, text: str, rules: EducationExtractionRules) -> str | None:
        """Detect degree using configurable degree indicators."""
        for indicator in rules.degree_indicators:
            escaped = re.escape(indicator)
            pattern = re.compile(
                rf"(\b{escaped}\b\.?\s*(?:of\s+)?[A-Za-z\s.]*)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                result = match.group(0).strip().rstrip(",.-")
                if len(result) >= len(indicator):
                    return result
        return None

    @classmethod
    def _detect_major(cls, text: str, rules: EducationExtractionRules) -> str | None:
        """Detect major/specialization using configurable major indicators."""
        for indicator in rules.major_indicators:
            pattern = re.compile(
                rf"\b{re.escape(indicator)}\b\s+([A-Z][A-Za-z\s&,]+)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                result = match.group(1).strip().rstrip(",.-")
                if len(result) > 2:
                    return result
        return None

    @classmethod
    def _detect_gpa(cls, text: str, rules: EducationExtractionRules) -> str | None:
        """Detect GPA/CGPA using configurable patterns."""
        for pat_str in rules.gpa_patterns:
            pattern = re.compile(pat_str, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return None

    @classmethod
    def _detect_grade(cls, text: str, rules: EducationExtractionRules) -> str | None:
        """Detect grade/class using configurable patterns."""
        for pat_str in rules.grade_patterns:
            pattern = re.compile(pat_str, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return None
