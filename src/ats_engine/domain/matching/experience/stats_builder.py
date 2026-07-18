"""Structural statistics builder for Experience matches.

Purpose:
    Compile standardized metrics tracking execution counts, processing durations,
    and match tallies using the unified telemetry schema.
"""

from __future__ import annotations

from typing import Any, Mapping


class ExperienceMatchStatisticsBuilder:
    """Builder compiling structural metrics for Experience matching execution runs."""

    @classmethod
    def build(
        cls,
        total_resume_features: int,
        total_job_features: int,
        candidate_pairs: int,
        matched_pairs: int,
        skipped_candidates: int,
        validation_failures: int,
        comparison_mode: str,
        execution_duration_ms: float,
    ) -> Mapping[str, Any]:
        """Compile matching execution stats map using the standardized schema.

        Args:
            total_resume_features: Count of resume features entering the matcher.
            total_job_features: Count of job features entering the matcher.
            candidate_pairs: Total candidate pairs generated.
            matched_pairs: Total successful matches.
            skipped_candidates: Empty candidates filtered out.
            validation_failures: Candidates failing structural validation.
            comparison_mode: Active comparison mode string.
            execution_duration_ms: Pipeline process duration in milliseconds.

        Returns:
            A dictionary containing standardized match statistics.
        """
        return {
            "total_resume_features": total_resume_features,
            "total_job_features": total_job_features,
            "candidate_pairs": candidate_pairs,
            "matched_pairs": matched_pairs,
            "skipped_candidates": skipped_candidates,
            "validation_failures": validation_failures,
            "comparison_mode": comparison_mode,
            "execution_duration_ms": execution_duration_ms,
        }
