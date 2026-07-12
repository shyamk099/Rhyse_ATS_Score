"""Experience candidate builder.

Purpose:
    Scan permitted sections and segments for date ranges, company indicators,
    role indicators, and employment type markers to build raw candidates.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCandidate
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class ExperienceCandidateBuilder:
    """Stateless builder scanning segments for experience evidence."""

    @classmethod
    def build_candidates(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: ExperienceExtractionRules,
    ) -> Sequence[ExperienceCandidate]:
        """Scan sections allowed by scope config and extract raw experience candidates.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            A sequence of discovered ExperienceCandidates.
        """
        candidates: list[ExperienceCandidate] = []
        scope = [s.upper() for s in rules.extraction_scope]
        scan_all = "ALL" in scope or not scope

        # Compile date patterns
        date_patterns = [re.compile(p, re.IGNORECASE) for p in rules.date_patterns]
        current_indicators = [ci.lower() for ci in rules.current_employment_indicators]

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

                # Detect current employment
                text_lower = text.lower()
                is_current = any(ci in text_lower for ci in current_indicators)

                # Detect company via configurable indicators
                detected_company = cls._detect_company(text, rules)

                # Detect role via configurable indicators
                detected_title = cls._detect_title(text, rules)

                # Detect employment type
                detected_emp_type = cls._detect_employment_type(text, rules)

                # Only create candidate if there's meaningful evidence
                if detected_dates or detected_company or detected_title:
                    candidates.append(
                        ExperienceCandidate(
                            segment_id=segment.segment_id,
                            section_type=section.section_type,
                            raw_text=text,
                            start_char=0,
                            end_char=len(text),
                            detected_dates=tuple(detected_dates),
                            detected_company=detected_company,
                            detected_title=detected_title,
                            detected_employment_type=detected_emp_type,
                            is_current=is_current,
                        )
                    )

        return candidates

    @classmethod
    def _detect_company(cls, text: str, rules: ExperienceExtractionRules) -> str | None:
        """Detect company name using configurable company indicators."""
        for indicator in rules.company_indicators:
            pattern = re.compile(
                rf"([A-Z][A-Za-z0-9\s&.-]*\b{re.escape(indicator)}\b\.?)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return None

    @classmethod
    def _detect_title(cls, text: str, rules: ExperienceExtractionRules) -> str | None:
        """Detect job title using configurable role indicators."""
        for indicator in rules.role_indicators:
            pattern = re.compile(
                rf"(\b(?:Senior|Junior|Lead|Staff|Principal|Chief)?\s*\w*\s*{re.escape(indicator)}\b)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return None

    @classmethod
    def _detect_employment_type(
        cls, text: str, rules: ExperienceExtractionRules
    ) -> str | None:
        """Detect employment type using configurable mappings."""
        text_lower = text.lower()
        for key, canonical in rules.employment_type_mappings.items():
            if key.lower() in text_lower:
                return canonical
        return None
