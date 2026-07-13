"""Certification candidate validator.

Purpose:
    Validate that a certification candidate has minimum required evidence
    (at least a certification name or issuing organization detected).
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCandidate
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules


class CertificationCandidateValidator:
    """Stateless validator checking certification candidates for minimum evidence."""

    @classmethod
    def validate(cls, candidate: CertificationCandidate, rules: CertificationExtractionRules) -> bool:
        """Validate that candidate contains minimal meaningful evidence.

        Args:
            candidate: Discovered certification candidate.
            rules: Configured extraction rules.

        Returns:
            True if candidate has sufficient evidence, False otherwise.
        """
        has_name = candidate.detected_name is not None
        has_issuer = candidate.detected_issuer is not None

        # Accept if certification name or issuing organization is present
        if has_name or has_issuer:
            return True

        return False
