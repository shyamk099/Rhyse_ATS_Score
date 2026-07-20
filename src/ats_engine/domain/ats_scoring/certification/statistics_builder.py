"""CertificationStatisticsBuilder definition.

Purpose:
    Provide telemetry statistics builder for CertificationScorer execution runs.
"""

from __future__ import annotations

from typing import Any


class CertificationStatisticsBuilder:
    """Builder generating stats dict metrics for Certification Scorer execution."""

    @staticmethod
    def build(
        matched_items: int = 0,
        missing_items: int = 0,
        exact_matches: int = 0,
        equivalent_certifications: int = 0,
        related_certifications: int = 0,
        partial_matches: int = 0,
        expired_certifications: int = 0,
        processing_time_ms: float = 0.0,
    ) -> dict[str, Any]:
        """Compile a dictionary containing operational metrics of Certification scoring."""
        return {
            "matched_items": matched_items,
            "missing_items": missing_items,
            "exact_matches": exact_matches,
            "equivalent_certifications": equivalent_certifications,
            "related_certifications": related_certifications,
            "partial_matches": partial_matches,
            "expired_certifications": expired_certifications,
            "processing_time_ms": processing_time_ms,
        }

