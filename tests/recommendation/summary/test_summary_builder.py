"""Tests for ResumeSummaryBuilder.

Purpose:
    Verify builder correctly assembles health, section summaries, and top recommendations.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules
from ats_engine.domain.recommendation.summary.summary_builder import ResumeSummaryBuilder
from ats_engine.domain.recommendation.summary.summary_statistics_builder import ResumeIntelligenceStatisticsBuilder


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


def _make_orchestrated(
    recs: tuple[Recommendation, ...] = (),
    high: tuple[Recommendation, ...] = (),
    medium: tuple[Recommendation, ...] = (),
    low: tuple[Recommendation, ...] = (),
    by_section: dict | None = None,
    by_category: dict | None = None,
) -> OrchestratedRecommendationResult:
    return OrchestratedRecommendationResult(
        recommendations=recs,
        grouped_recommendations=by_category or {},
        recommendations_by_section=by_section or {},
        recommendations_by_priority={"High": high, "Medium": medium, "Low": low},
        statistics=OrchestrationStatistics(
            execution_time_ms=0.1,
            recommendations_processed=len(recs),
            sections=len(by_section) if by_section else 0,
            categories=len(by_category) if by_category else 0,
            high_priority=len(high),
            medium_priority=len(medium),
            low_priority=len(low),
            largest_section="",
            largest_category="",
            success=True,
        ),
        total_recommendations=len(recs),
    )


class SummaryBuilderTests(unittest.TestCase):
    """Test suite validating ResumeSummaryBuilder assembly logic."""

    def setUp(self) -> None:
        self.rules = PrioritizationRules()

    def test_build_health_no_high(self) -> None:
        """Zero high-priority recommendations must yield Excellent health."""
        health = ResumeSummaryBuilder.build_health({"High": (), "Medium": (), "Low": ()})
        self.assertEqual(100.0, health.score)
        self.assertEqual("A", health.grade)

    def test_build_health_with_high(self) -> None:
        """One high-priority recommendation must yield Good health."""
        r = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        health = ResumeSummaryBuilder.build_health({"High": (r,), "Medium": (), "Low": ()})
        self.assertEqual(85.0, health.score)
        self.assertEqual("B", health.grade)

    def test_build_section_summaries_empty(self) -> None:
        """Empty section mapping must produce empty summaries."""
        summaries = ResumeSummaryBuilder.build_section_summaries({}, self.rules)
        self.assertEqual(0, len(summaries))

    def test_build_section_summaries_multiple(self) -> None:
        """Section summaries must be sorted alphabetically and count correctly."""
        r1 = _make_rec("R1", "experience", "EXPERIENCE_MISSING", 95)
        r2 = _make_rec("R2", "skill", "SKILL_MISSING", 100)
        by_section = {"experience": (r1,), "skill": (r2,)}
        summaries = ResumeSummaryBuilder.build_section_summaries(by_section, self.rules)

        self.assertEqual(2, len(summaries))
        self.assertEqual("experience", summaries[0].section)
        self.assertEqual("skill", summaries[1].section)
        self.assertEqual(1, summaries[0].total_recommendations)
        self.assertEqual(1, summaries[0].high_priority)

    def test_build_top_recommendations_default(self) -> None:
        """Default top_n=5 must slice the first 5 recommendations."""
        recs = tuple(_make_rec(f"R{i}", "skill", "SKILL_MISSING", 100) for i in range(10))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(5, len(top))
        self.assertEqual("R0", top[0].recommendation_id)
        self.assertEqual("R4", top[4].recommendation_id)

    def test_build_top_recommendations_fewer_than_n(self) -> None:
        """Fewer than N recommendations must return all of them."""
        recs = tuple(_make_rec(f"R{i}", "skill", "SKILL_MISSING", 100) for i in range(3))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(3, len(top))

    def test_build_full_summary(self) -> None:
        """Full build must produce a valid ResumeIntelligenceSummary."""
        r1 = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        r2 = _make_rec("R2", "experience", "EXPERIENCE_PARTIAL_MATCH", 75)
        orchestrated = _make_orchestrated(
            recs=(r1, r2),
            high=(r1,),
            medium=(r2,),
            by_section={"skill": (r1,), "experience": (r2,)},
            by_category={"SKILL_MISSING": (r1,), "EXPERIENCE_PARTIAL_MATCH": (r2,)},
        )
        stats = ResumeIntelligenceStatisticsBuilder.build(
            execution_time_ms=0.1,
            sections_processed=2,
            recommendations_processed=2,
        )
        summary = ResumeSummaryBuilder.build(orchestrated, self.rules, stats)

        self.assertEqual(2, summary.total_recommendations)
        self.assertEqual(1, summary.high_priority)
        self.assertEqual(1, summary.medium_priority)
        self.assertEqual(0, summary.low_priority)
        self.assertEqual(2, len(summary.section_summaries))
        self.assertEqual(2, len(summary.top_recommendations))
        self.assertEqual(85.0, summary.overall_health.score)


if __name__ == "__main__":
    unittest.main()
