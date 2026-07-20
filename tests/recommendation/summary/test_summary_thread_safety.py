"""Tests for summary engine thread safety.

Purpose:
    Verify the summary engine produces consistent results under concurrent execution.
"""

from __future__ import annotations

import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine


def _make_rec(rec_id: str, section: str, priority: int) -> Recommendation:
    return Recommendation(
        recommendation_id=rec_id,
        section=section,
        category="SKILL_MISSING",
        title=f"Title {rec_id}",
        description=f"Description {rec_id}",
        priority=priority,
        impact=0.8,
        confidence=0.9,
    )


def _make_orchestrated() -> OrchestratedRecommendationResult:
    r1 = _make_rec("R1", "skill", 100)
    r2 = _make_rec("R2", "experience", 75)
    r3 = _make_rec("R3", "education", 50)
    recs = (r1, r2, r3)
    return OrchestratedRecommendationResult(
        recommendations=recs,
        grouped_recommendations={"SKILL_MISSING": recs},
        recommendations_by_section={
            "skill": (r1,),
            "experience": (r2,),
            "education": (r3,),
        },
        recommendations_by_priority={
            "High": (r1,),
            "Medium": (r2,),
            "Low": (r3,),
        },
        statistics=OrchestrationStatistics(
            execution_time_ms=0.1,
            recommendations_processed=3,
            sections=3,
            categories=1,
            high_priority=1,
            medium_priority=1,
            low_priority=1,
            largest_section="skill",
            largest_category="SKILL_MISSING",
            success=True,
        ),
        total_recommendations=3,
    )


class SummaryThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety of ResumeIntelligenceSummaryEngine."""

    def test_concurrent_processing(self) -> None:
        """Multiple threads must produce consistent results."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_orchestrated()
        num_threads = 8
        iterations_per_thread = 50

        def run_batch() -> list[tuple[int, int, float, str]]:
            results = []
            for _ in range(iterations_per_thread):
                r = engine.process(orchestrated)
                results.append((
                    r.total_recommendations,
                    r.high_priority,
                    r.overall_health.score,
                    r.overall_health.grade,
                ))
            return results

        all_results: list[tuple[int, int, float, str]] = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(run_batch) for _ in range(num_threads)]
            for future in as_completed(futures):
                all_results.extend(future.result())

        self.assertEqual(num_threads * iterations_per_thread, len(all_results))
        # All results must be identical
        for total, high, score, grade in all_results:
            self.assertEqual(3, total)
            self.assertEqual(1, high)
            self.assertEqual(85.0, score)
            self.assertEqual("B", grade)

    def test_no_shared_state_corruption(self) -> None:
        """Concurrent access must not corrupt engine state."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_orchestrated()

        exceptions: list[Exception] = []

        def process_and_validate() -> None:
            try:
                result = engine.process(orchestrated)
                assert result.total_recommendations == 3
                assert result.high_priority + result.medium_priority + result.low_priority == 3
            except Exception as e:
                exceptions.append(e)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_and_validate) for _ in range(100)]
            for f in as_completed(futures):
                f.result()

        self.assertEqual(0, len(exceptions), f"Exceptions occurred: {exceptions}")


if __name__ == "__main__":
    unittest.main()
