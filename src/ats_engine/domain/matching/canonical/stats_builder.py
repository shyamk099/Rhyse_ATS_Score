"""MatchStatistics builder for CanonicalMatchCollection.

Purpose:
    Compile structural metadata and counts regarding match results, categories,
    duplicates, warnings, errors, and execution metrics.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from ats_engine.domain.matching.models import MatchResult, MatchStatistics


class MatchStatisticsBuilder:
    """Builder compiling structural metrics for CanonicalMatchCollections."""

    @classmethod
    def build(
        cls,
        results: Sequence[MatchResult],
        total_resume_features: int,
        total_job_features: int,
        duplicate_count: int,
        validation_error_count: int,
        warning_count: int,
        execution_duration_ms: float,
    ) -> MatchStatistics:
        """Compile execution statistics.

        Args:
            results: Sequence of validated/resolved MatchResults.
            total_resume_features: Aggregated resume feature count.
            total_job_features: Aggregated job feature count.
            duplicate_count: Total duplicate matches resolved/skipped.
            validation_error_count: Total structural validation errors found.
            warning_count: Total warnings generated.
            execution_duration_ms: Time duration in milliseconds.

        Returns:
            A frozen MatchStatistics instance.
        """
        category_counts: dict[str, int] = {}
        for r in results:
            cat = r.matcher_type or "Unknown"
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return MatchStatistics(
            total_resume_features=total_resume_features,
            total_job_features=total_job_features,
            total_matches=len(results),
            duplicate_count=duplicate_count,
            validation_error_count=validation_error_count,
            warning_count=warning_count,
            category_counts=category_counts,
            execution_duration_ms=execution_duration_ms,
        )
