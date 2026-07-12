"""Education candidate validator.

Purpose:
    Validate that an education candidate has minimum required evidence
    (at least a degree or institution name detected).
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.education.education_models import EducationCandidate
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules


class EducationCandidateValidator:
    """Stateless validator checking education candidates for minimum evidence."""

    @classmethod
    def validate(cls, candidate: EducationCandidate, rules: EducationExtractionRules) -> bool:
        """Validate that candidate contains minimal meaningful evidence.

        Args:
            candidate: Discovered education candidate.
            rules: Configured extraction rules.

        Returns:
            True if candidate has sufficient evidence, False otherwise.
        """
        has_degree = candidate.detected_degree is not None
        has_institution = candidate.detected_institution is not None

        # Accept if degree or institution is present
        if has_degree or has_institution:
            return True

        # Reject candidates that only have GPA or grade but no degree/institution
        return False
