"""CertificationRecommendationBuilder definition.

Purpose:
    Isolate construction logic for certification recommendations.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.recommendation.models import Recommendation


class CertificationRecommendationBuilder:
    """Builder producing deterministic Recommendation DTOs for Certification features."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Helper to normalize names into deterministic ID components."""
        return name.upper().strip().replace(" ", "_").replace("-", "_")

    @classmethod
    def build_missing_recommendation(
        cls,
        certification_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for a missing certification requirement.

        Args:
            certification_name: The name of the missing certification requirement.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(certification_name)
        rec_id = f"CERT_MISSING_{norm_name}"
        title = f"{certification_name} certification is missing"
        description = f"The job description requires {certification_name} certification but it was not found in the resume."

        return Recommendation(
            recommendation_id=rec_id,
            section="certification",
            category="CERTIFICATION_MISSING",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_partial_recommendation(
        cls,
        certification_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for partially matched certification.

        Args:
            certification_name: The name of the partially matched certification.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(certification_name)
        rec_id = f"CERT_PARTIAL_{norm_name}"
        title = f"Expand {certification_name} details"
        description = f"The resume contains a related or partially matching certification for {certification_name}."

        return Recommendation(
            recommendation_id=rec_id,
            section="certification",
            category="CERTIFICATION_PARTIAL_MATCH",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )

    @classmethod
    def build_expired_recommendation(
        cls,
        certification_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Recommendation:
        """Construct a Recommendation DTO for an expired certification.

        Args:
            certification_name: The name of the expired certification.
            metadata: Optional metadata attributes.

        Returns:
            A populated Recommendation DTO.
        """
        norm_name = cls._normalize_name(certification_name)
        rec_id = f"CERT_EXPIRED_{norm_name}"
        title = f"Renew {certification_name} certification"
        description = f"The resume contains {certification_name} but it is marked as expired."

        return Recommendation(
            recommendation_id=rec_id,
            section="certification",
            category="CERTIFICATION_EXPIRED",
            title=title,
            description=description,
            priority=0,
            impact=0.0,
            confidence=1.0,
            metadata=metadata or {},
        )
