"""Experience candidate validator.

Purpose:
    Validate that an experience candidate has minimum required evidence
    (at least a job title or company name detected).
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCandidate
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules


class ExperienceCandidateValidator:
    """Stateless validator checking experience candidates for minimum evidence."""

    @classmethod
    def validate(cls, candidate: ExperienceCandidate, rules: ExperienceExtractionRules) -> bool:
        """Validate that candidate contains minimal meaningful evidence.

        Args:
            candidate: Discovered experience candidate.
            rules: Configured extraction rules.

        Returns:
            True if candidate has sufficient evidence, False otherwise.
        """
        # Require at least a title or a company to form a valid experience entry
        has_title = candidate.detected_title is not None
        has_company = candidate.detected_company is not None
        has_dates = len(candidate.detected_dates) > 0

        # Accept if title or company is present alongside any date evidence
        if has_title or has_company:
            return True

        # Reject candidates that only have dates but no title/company context
        return False
