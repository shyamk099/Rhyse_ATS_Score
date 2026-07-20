"""ResumeHealthPolicy definition.

Purpose:
    Isolate deterministic health rules from summary construction.
    The policy maps high-priority recommendation counts to a ResumeHealth DTO
    containing score, grade, and status.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.summary.models import ResumeHealth


class ResumeHealthPolicy:
    """Deterministic policy mapping high-priority counts to ResumeHealth.

    Thresholds:
        0 high priority     → 100.0, A, Excellent
        1–2 high priority   → 85.0,  B, Good
        3–5 high priority   → 70.0,  C, Needs Improvement
        >5 high priority    → 50.0,  D, Critical

    This class is the single source of truth for health classification.
    """

    @staticmethod
    def evaluate(high_priority_count: int) -> ResumeHealth:
        """Evaluate resume health from high-priority recommendation count.

        Args:
            high_priority_count: Number of high-priority recommendations.

        Returns:
            An immutable ResumeHealth DTO.

        Raises:
            ValueError: If high_priority_count is negative.
        """
        if high_priority_count < 0:
            raise ValueError(
                f"high_priority_count must be non-negative, got {high_priority_count}"
            )

        if high_priority_count == 0:
            return ResumeHealth(score=100.0, grade="A", status="Excellent")
        if high_priority_count <= 2:
            return ResumeHealth(score=85.0, grade="B", status="Good")
        if high_priority_count <= 5:
            return ResumeHealth(score=70.0, grade="C", status="Needs Improvement")
        return ResumeHealth(score=50.0, grade="D", status="Critical")
