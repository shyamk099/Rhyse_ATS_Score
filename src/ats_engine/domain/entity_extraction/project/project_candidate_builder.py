"""Project candidate builder.

Purpose:
    Scan permitted sections and segments for project titles, roles,
    organizations/clients, date ranges, repository URLs, and demo URLs
    to build raw project candidates.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.project.project_models import ProjectCandidate
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection


class ProjectCandidateBuilder:
    """Stateless builder scanning segments for project evidence."""

    @classmethod
    def build_candidates(
        cls,
        document: CanonicalDocument,
        sections: SectionCollection,
        rules: ProjectExtractionRules,
    ) -> Sequence[ProjectCandidate]:
        """Scan sections allowed by scope config and extract raw project candidates.

        Args:
            document: The CanonicalDocument resource.
            sections: The SectionCollection logical grouping.
            rules: Configured extraction rules.

        Returns:
            A sequence of discovered ProjectCandidates.
        """
        candidates: list[ProjectCandidate] = []
        scope = [s.upper() for s in rules.extraction_scope]
        scan_all = "ALL" in scope or not scope

        # Compile date patterns
        date_patterns = [re.compile(p, re.IGNORECASE) for p in rules.date_patterns]

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

                # Detect URLs based on rule-defined domains
                detected_repo = cls._detect_repo_url(text, rules)
                detected_demo = cls._detect_demo_url(text, rules)

                # Detect project name / title (without inferring from URL)
                detected_name = cls._detect_name(text, rules)

                # Detect organization / client
                detected_org = cls._detect_organization(text, rules)

                # Detect role
                detected_role = cls._detect_role(text, rules)

                # Accept candidate if there's meaningful evidence (name or role or url)
                if detected_name or detected_role or detected_repo or detected_demo:
                    candidates.append(
                        ProjectCandidate(
                            segment_id=segment.segment_id,
                            section_type=section.section_type,
                            raw_text=text,
                            start_char=0,
                            end_char=len(text),
                            detected_dates=tuple(detected_dates),
                            detected_name=detected_name,
                            detected_organization=detected_org,
                            detected_role=detected_role,
                            detected_repo_url=detected_repo,
                            detected_demo_url=detected_demo,
                        )
                    )

        return candidates

    @classmethod
    def _detect_repo_url(cls, text: str, rules: ProjectExtractionRules) -> str | None:
        """Detect repository URL using domains from Rules."""
        for domain in rules.repository_domains:
            # Match domain followed by paths
            pattern = re.compile(
                rf"(https?://(?:www\.)?{re.escape(domain)}/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return None

    @classmethod
    def _detect_demo_url(cls, text: str, rules: ProjectExtractionRules) -> str | None:
        """Detect demo URL using domains from Rules."""
        for domain in rules.demo_domains:
            pattern = re.compile(
                rf"(https?://(?:www\.)?[A-Za-z0-9.-]*{re.escape(domain)}[^\s]*)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(1).strip().rstrip(",.()[]{}")
        return None

    @classmethod
    def _detect_name(cls, text: str, rules: ProjectExtractionRules) -> str | None:
        """Detect project name using title indicators (never infer from URLs)."""
        lines = text.split("\n")
        first_line = lines[0].strip() if lines else ""

        # First, look at the first line. Ensure it doesn't look like a URL
        if first_line.startswith(("http://", "https://", "www.")):
            first_line = ""

        if first_line:
            # Check if first line contains any project title indicators
            for indicator in rules.project_title_indicators:
                if indicator.lower() in first_line.lower():
                    return first_line.rstrip(",:-–— ")

        # Look anywhere in text for indicator
        for indicator in rules.project_title_indicators:
            pattern = re.compile(
                rf"([A-Z][A-Za-z0-9\s&.-]*\b{re.escape(indicator)}\b)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                val = match.group(1).strip()
                if not val.startswith(("http://", "https://", "www.")):
                    return val.rstrip(",:-–— ")

        # Fallback to first line if it looks like a valid title
        if 0 < len(first_line) < 50 and any(c.isupper() for c in first_line):
            return first_line.rstrip(",:-–— ")

        return None

    @classmethod
    def _detect_organization(cls, text: str, rules: ProjectExtractionRules) -> str | None:
        """Detect organization / client using organization indicators."""
        for indicator in rules.organization_indicators:
            pattern = re.compile(
                rf"\b{re.escape(indicator)}\b\s+([A-Z][A-Za-z0-9\s&.-]+)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                result = match.group(1).strip().split("\n")[0]
                return result.rstrip(",.- ")
        return None

    @classmethod
    def _detect_role(cls, text: str, rules: ProjectExtractionRules) -> str | None:
        """Detect role in project using role indicators."""
        for indicator in rules.role_indicators:
            pattern = re.compile(
                rf"(\b(?:Senior|Junior|Lead|Solo)?\s*{re.escape(indicator)}\b)",
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return match.group(0).strip()
        return None
