"""Heading candidate validator.

Purpose:
    Perform sanity validation on identified section heading candidates.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.section.section_models import SectionCandidate
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules


class HeadingValidator:
    """Stateless validator auditing heading candidate formatting constraints."""

    @classmethod
    def validate(cls, candidate: SectionCandidate, rules: SectionDetectionRules) -> bool:
        """Validate heading candidate format.

        Args:
            candidate: Discovered SectionCandidate.
            rules: Configured heading rules.

        Returns:
            True if candidate is valid, False otherwise.
        """
        text = candidate.matched_text.strip()
        
        # Heading must not be empty
        if not text:
            return False

        # Heading must not exceed configured max word length
        words = text.split()
        if len(words) > rules.max_heading_words:
            return False

        # Filter out purely numeric text (e.g. line numbers or values)
        if text.replace(".", "").replace("-", "").isdigit():
            return False

        return True
