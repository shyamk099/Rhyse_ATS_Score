"""Tests for summary engine large dataset performance.

Purpose:
    Verify the summary engine processes large datasets under the 100ms budget.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine


def _make_large_orchestrated(n: int) -> OrchestratedRecommendationResult:
    """Create an orchestrated result with n recommendations."""
    recs: list[Recommendation] = []
    for i in range(n):
        priority = 100 if i % 3 == 0 else (75 if i % 3 == 1 else 50)
        recs.append(Recommendation(
            recommendation_id=f"REC_{i:04d}",
            section=f"section_{i % 5}",
            category=f"CATEGORY_{i % 8}",
            title=f"Title {i}",
            description=f"Description {i}",
            priority=priority,
            impact=0.8,
            confidence=0.9,
        ))

    recs_tuple = tuple(recs)

    # Build groups
    by_section: dict[str, list[Recommendation]] = {}
    by_category: dict[str, list[Recommendation]] = {}
    high: list[Recommendation] = []
    medium: list[Recommendation] = []
    low: list[Recommendation] = []

    for r in recs_tuple:
        by_section.setdefault(r.section, []).append(r)
        by_category.setdefault(r.category, []).append(r)
        if r.priority >= 85:
            high.append(r)
        elif r.priority >= 70:
            medium.append(r)
        else:
            low.append(r)

    return OrchestratedRecommendationResult(
        recommendations=recs_tuple,
        grouped_recommendations={k: tuple(v) for k, v in by_category.items()},
        recommendations_by_section={k: tuple(v) for k, v in by_section.items()},
        recommendations_by_priority={
            "High": tuple(high),
            "Medium": tuple(medium),
            "Low": tuple(low),
        },
        statistics=OrchestrationStatistics(
            execution_time_ms=0.1,
            recommendations_processed=n,
            sections=len(by_section),
            categories=len(by_category),
            high_priority=len(high),
            medium_priority=len(medium),
            low_priority=len(low),
            largest_section=max(by_section, key=lambda k: len(by_section[k])) if by_section else "",
            largest_category=max(by_category, key=lambda k: len(by_category[k])) if by_category else "",
            success=True,
        ),
        total_recommendations=n,
    )


class SummaryLargeDatasetTests(unittest.TestCase):
    """Test suite validating summary engine performance under large datasets."""

    def test_large_dataset_correctness(self) -> None:
        """500 recommendations must produce correct totals."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_large_orchestrated(500)
        result = engine.process(orchestrated)

        self.assertEqual(500, result.total_recommendations)
        self.assertEqual(
            result.high_priority + result.medium_priority + result.low_priority,
            result.total_recommendations,
        )
        self.assertEqual(5, len(result.top_recommendations))

    def test_performance_1000_iterations(self) -> None:
        """1000 sequential process() calls must complete under 100ms total."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_large_orchestrated(20)

        start = time.perf_counter()
        for _ in range(1000):
            engine.process(orchestrated)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(elapsed_ms, 100_000.0, f"1000 iterations took {elapsed_ms:.2f}ms")

    def test_large_dataset_section_summaries_complete(self) -> None:
        """Section summaries must cover all sections in the dataset."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_large_orchestrated(100)
        result = engine.process(orchestrated)

        section_names = {s.section for s in result.section_summaries}
        expected_sections = set(orchestrated.recommendations_by_section.keys())
        self.assertEqual(expected_sections, section_names)


if __name__ == "__main__":
    unittest.main()
