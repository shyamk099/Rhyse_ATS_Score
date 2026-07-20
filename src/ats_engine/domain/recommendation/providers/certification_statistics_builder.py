"""CertificationRecommendationStatisticsBuilder definition.

Purpose:
    Compile certification recommendation provider execution statistics.
"""

from __future__ import annotations

from typing import Any


class CertificationRecommendationStatisticsBuilder:
    """Builder compiling execution metrics for CertificationRecommendationProvider."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        certifications_processed: int = 0,
        missing_certifications: int = 0,
        partial_matches: int = 0,
        expired_certifications: int = 0,
        exact_matches: int = 0,
        equivalent_matches: int = 0,
        recommendations_generated: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Time taken to run the provider.
            certifications_processed: Total number of certification features processed.
            missing_certifications: Number of missing certification requirements.
            partial_matches: Number of partial matches.
            expired_certifications: Number of expired certifications.
            exact_matches: Number of exact matches.
            equivalent_matches: Number of equivalent matches.
            recommendations_generated: Number of recommendations generated.
            success: Whether the provider completed successfully.

        Returns:
            A dictionary with the statistics.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "certifications_processed": certifications_processed,
            "missing_certifications": missing_certifications,
            "partial_matches": partial_matches,
            "expired_certifications": expired_certifications,
            "exact_matches": exact_matches,
            "equivalent_matches": equivalent_matches,
            "recommendations_generated": recommendations_generated,
            "success": success,
        }
