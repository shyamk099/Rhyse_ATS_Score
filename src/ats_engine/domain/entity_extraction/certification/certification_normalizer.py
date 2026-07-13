"""Certification normalizer.

Purpose:
    Normalize raw fields: split raw date pairs into issue/expiration,
    and normalize credential URLs preserving their provenance.
    No date interpretation.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.certification.certification_models import (
    CertificationCandidate,
    NormalizedCertification,
    CertificationURL,
)
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules
from ats_engine.domain.entity_extraction.certification.exceptions import CertificationNormalizationError


class CertificationNormalizer:
    """Stateless normalizer transforming raw evidence into cleaned intermediate forms."""

    @classmethod
    def normalize(
        cls, candidate: CertificationCandidate, rules: CertificationExtractionRules
    ) -> NormalizedCertification:
        """Normalize raw candidate fields and build CertificationURL objects.

        Args:
            candidate: Validated certification candidate.
            rules: Configured extraction rules.

        Returns:
            The NormalizedCertification metadata container.

        Raises:
            CertificationNormalizationError: If normalization encounters failures.
        """
        try:
            issue_date_raw, expiration_date_raw = cls._split_dates(candidate, rules)

            cred_url = None
            if candidate.detected_credential_url:
                # Resolve matched rule
                matched_rule = "generic_credential_url_rule"
                for pat in rules.credential_url_patterns:
                    if pat in rules.credential_url_patterns:
                        matched_rule = "configured_credential_url_pattern"
                        break
                cred_url = CertificationURL(
                    original_value=candidate.detected_credential_url,
                    normalized_value=candidate.detected_credential_url.lower(),
                    matched_rule=matched_rule,
                )

            return NormalizedCertification(
                candidate=candidate,
                certification_name=candidate.detected_name,
                issuing_organization=candidate.detected_issuer,
                credential_id_raw=candidate.detected_credential_id,
                credential_url=cred_url,
                issue_date_raw=issue_date_raw,
                expiration_date_raw=expiration_date_raw,
                validity_status_raw=None,  # Derived in feature engineering
            )
        except Exception as error:
            raise CertificationNormalizationError(
                f"Failed to normalize certification candidate: {error}"
            ) from error

    @classmethod
    def _split_dates(
        cls, candidate: CertificationCandidate, rules: CertificationExtractionRules
    ) -> tuple[str | None, str | None]:
        """Split detected dates into issue and expiration raw strings."""
        dates = list(candidate.detected_dates)
        if not dates:
            return None, None
        if len(dates) == 1:
            return dates[0], None
        return dates[0], dates[1]
