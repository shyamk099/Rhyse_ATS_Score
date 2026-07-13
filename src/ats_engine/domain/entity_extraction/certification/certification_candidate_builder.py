"""Certification candidate builder.

Purpose:
    Scan permitted sections and segments for certification names, issuing
    organizations, credential IDs, credential URLs, and date ranges
    to build raw certification candidates.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCandidate
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class CertificationCandidateBuilder:
    """Stateless builder scanning segments for certification evidence."""

    @classmethod
    def build_candidates(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: CertificationExtractionRules,
    ) -> Sequence[CertificationCandidate]:
        """Scan sections allowed by scope config and extract raw certification candidates.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            A sequence of discovered CertificationCandidates.
        """
        candidates: list[CertificationCandidate] = []
        scope = [s.upper() for s in rules.extraction_scope]
        scan_all = "ALL" in scope or not scope

        # Compile patterns
        date_patterns = [re.compile(p, re.IGNORECASE) for p in rules.date_patterns]
        url_patterns = [re.compile(p, re.IGNORECASE) for p in rules.credential_url_patterns]
        id_patterns = [re.compile(p, re.IGNORECASE) for p in rules.credential_id_patterns]

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

                # Detect Credential URL
                detected_url = None
                for pat in url_patterns:
                    match = pat.search(text)
                    if match:
                        detected_url = match.group(0).strip()
                        break

                # Detect Credential ID
                detected_id = None
                for pat in id_patterns:
                    match = pat.search(text)
                    if match:
                        # If there is a capture group, use it, otherwise use the whole match
                        detected_id = match.group(1).strip() if match.groups() else match.group(0).strip()
                        break

                # Detect name / indicator
                detected_name = cls._detect_name(text, rules)

                # Detect issuer / organization
                detected_issuer = cls._detect_issuer(text, rules)

                # Accept candidate if name or issuer or url or id is detected
                if detected_name or detected_issuer or detected_url or detected_id:
                    candidates.append(
                        CertificationCandidate(
                            segment_id=segment.segment_id,
                            section_type=section.section_type,
                            raw_text=text,
                            start_char=0,
                            end_char=len(text),
                            detected_dates=tuple(detected_dates),
                            detected_name=detected_name,
                            detected_issuer=detected_issuer,
                            detected_credential_id=detected_id,
                            detected_credential_url=detected_url,
                        )
                    )

        return candidates

    @classmethod
    def _detect_name(cls, text: str, rules: CertificationExtractionRules) -> str | None:
        """Detect certification name using certification indicators."""
        lines = text.split("\n")
        first_line = lines[0].strip() if lines else ""

        # Check if first line contains any indicators
        for indicator in rules.certification_indicators:
            if indicator.lower() in first_line.lower():
                return first_line.rstrip(",:-–— ")

        # Look in the text for indicator match
        for indicator in rules.certification_indicators:
            pattern = re.compile(
                rf"([A-Z][A-Za-z0-9\s&.-]*\b{re.escape(indicator)}\b[A-Za-z0-9\s&.-]*)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(0).strip().rstrip(",:-–— ")

        # Fallback to first line if short and capitalized
        if 0 < len(first_line) < 60 and any(c.isupper() for c in first_line):
            return first_line.rstrip(",:-–— ")

        return None

    @classmethod
    def _detect_issuer(cls, text: str, rules: CertificationExtractionRules) -> str | None:
        """Detect issuing organization using organization indicators."""
        for indicator in rules.issuing_organization_indicators:
            # Check prefix phrase match: e.g. "issued by Scrum Alliance"
            pattern = re.compile(
                rf"\b{re.escape(indicator)}\b\s+([A-Z][A-Za-z0-9\s&.-]+)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                result = match.group(1).strip().split("\n")[0]
                return result.rstrip(",.- ")
            
            # Check exact match: e.g. "Scrum Alliance" directly mentioned in text
            if len(indicator) > 3 and indicator.lower() in text.lower():
                pattern_exact = re.compile(rf"\b{re.escape(indicator)}\b", re.IGNORECASE)
                match_exact = pattern_exact.search(text)
                if match_exact:
                    return match_exact.group(0).strip()

        return None
