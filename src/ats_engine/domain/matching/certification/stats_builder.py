"""Structural statistics builder for Certification matches.

Purpose:
    Compile standardized metrics tracking execution counts, processing durations,
    and match tallies using the unified telemetry schema.
"""

from __future__ import annotations

from typing import Any, Mapping


class CertificationMatchStatisticsBuilder:
    """Builder compiling structural metrics for Certification matching execution runs."""

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
        """Compile matching execution stats map using the standardized schema."""
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
