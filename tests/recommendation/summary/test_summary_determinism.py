"""Tests for summary determinism.

Purpose:
    Verify that identical inputs produce identical outputs across multiple runs.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine


def _make_rec(rec_id: str, section: str, category: str, priority: int) -> Recommendation:
    return Recommendation(
        recommendation_id=rec_id,
        section=section,
        category=category,
        title=f"Title {rec_id}",
        description=f"Description {rec_id}",
        priority=priority,
        impact=0.8,
        confidence=0.9,
    )


def _make_orchestrated() -> OrchestratedRecommendationResult:
    r1 = _make_rec("R1", "skill", "SKILL_MISSING", 100)
    r2 = _make_rec("R2", "experience", "EXPERIENCE_MISSING", 95)
    r3 = _make_rec("R3", "education", "EDUCATION_PARTIAL_MATCH", 55)
    recs = (r1, r2, r3)
    return OrchestratedRecommendationResult(
        recommendations=recs,
        grouped_recommendations={
            "SKILL_MISSING": (r1,),
            "EXPERIENCE_MISSING": (r2,),
            "EDUCATION_PARTIAL_MATCH": (r3,),
        },
        recommendations_by_section={
            "skill": (r1,),
            "experience": (r2,),
            "education": (r3,),
        },
        recommendations_by_priority={
            "High": (r1, r2),
            "Medium": (),
            "Low": (r3,),
        },
        statistics=OrchestrationStatistics(
            execution_time_ms=0.1,
            recommendations_processed=3,
            sections=3,
            categories=3,
            high_priority=2,
            medium_priority=0,
            low_priority=1,
            largest_section="skill",
            largest_category="SKILL_MISSING",
            success=True,
        ),
        total_recommendations=3,
    )


class SummaryDeterminismTests(unittest.TestCase):
    """Test suite validating deterministic summary output."""

    def test_identical_inputs_produce_identical_outputs(self) -> None:
        """Multiple runs with the same input must produce identical summary structure."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_orchestrated()

        results = [engine.process(orchestrated) for _ in range(10)]

        for r in results[1:]:
            self.assertEqual(results[0].total_recommendations, r.total_recommendations)
            self.assertEqual(results[0].high_priority, r.high_priority)
            self.assertEqual(results[0].medium_priority, r.medium_priority)
            self.assertEqual(results[0].low_priority, r.low_priority)
            self.assertEqual(results[0].overall_health.score, r.overall_health.score)
            self.assertEqual(results[0].overall_health.grade, r.overall_health.grade)
            self.assertEqual(results[0].overall_health.status, r.overall_health.status)
            self.assertEqual(len(results[0].section_summaries), len(r.section_summaries))
            self.assertEqual(len(results[0].top_recommendations), len(r.top_recommendations))
            for s0, si in zip(results[0].section_summaries, r.section_summaries):
                self.assertEqual(s0.section, si.section)
                self.assertEqual(s0.total_recommendations, si.total_recommendations)
                self.assertEqual(s0.high_priority, si.high_priority)
                self.assertEqual(s0.medium_priority, si.medium_priority)
                self.assertEqual(s0.low_priority, si.low_priority)

    def test_section_summaries_sorted_deterministically(self) -> None:
        """Section summaries must always be sorted alphabetically."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_orchestrated()
        result = engine.process(orchestrated)

        sections = [s.section for s in result.section_summaries]
        self.assertEqual(sorted(sections), sections)

    def test_top_recommendations_order_stable(self) -> None:
        """Top recommendations must always follow the same order."""
        engine = ResumeIntelligenceSummaryEngine()
        orchestrated = _make_orchestrated()

        results = [engine.process(orchestrated) for _ in range(5)]
        for r in results[1:]:
            for t0, ti in zip(results[0].top_recommendations, r.top_recommendations):
                self.assertEqual(t0.recommendation_id, ti.recommendation_id)


if __name__ == "__main__":
    unittest.main()
