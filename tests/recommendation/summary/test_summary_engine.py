"""Tests for ResumeIntelligenceSummaryEngine.

Purpose:
    Verify summary engine post-processor executing builder, validator, and stats.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine
from ats_engine.domain.recommendation.summary.models import ResumeIntelligenceSummary


def _make_orchestrated(
    recs: tuple[Recommendation, ...] = (),
    high: tuple[Recommendation, ...] = (),
    medium: tuple[Recommendation, ...] = (),
    low: tuple[Recommendation, ...] = (),
    by_section: dict | None = None,
    by_category: dict | None = None,
) -> OrchestratedRecommendationResult:
    """Helper to build an OrchestratedRecommendationResult for tests."""
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


class SummaryEngineTests(unittest.TestCase):
    """Test suite validating ResumeIntelligenceSummaryEngine execution."""

    def setUp(self) -> None:
        self.engine = ResumeIntelligenceSummaryEngine()

    def test_process_empty_orchestrated_result(self) -> None:
        """Processing an empty orchestrated result must produce an empty summary."""
        orchestrated = _make_orchestrated()
        result = self.engine.process(orchestrated)

        self.assertIsInstance(result, ResumeIntelligenceSummary)
        self.assertEqual(0, result.total_recommendations)
        self.assertEqual(0, result.high_priority)
        self.assertEqual(0, result.medium_priority)
        self.assertEqual(0, result.low_priority)
        self.assertEqual(0, len(result.top_recommendations))
        self.assertEqual(0, len(result.section_summaries))
        self.assertEqual(100.0, result.overall_health.score)
        self.assertEqual("A", result.overall_health.grade)
        self.assertEqual("Excellent", result.overall_health.status)
        self.assertTrue(result.statistics.summary_generated)

    def test_process_single_high_priority(self) -> None:
        """A single high-priority recommendation must yield Good health."""
        rec = _make_rec("REC_1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(
            recs=(rec,),
            high=(rec,),
            by_section={"skill": (rec,)},
            by_category={"SKILL_MISSING": (rec,)},
        )
        result = self.engine.process(orchestrated)

        self.assertEqual(1, result.total_recommendations)
        self.assertEqual(1, result.high_priority)
        self.assertEqual(85.0, result.overall_health.score)
        self.assertEqual("B", result.overall_health.grade)
        self.assertEqual("Good", result.overall_health.status)
        self.assertEqual(1, len(result.top_recommendations))

    def test_process_mixed_priorities(self) -> None:
        """Mixed priorities must group and count correctly."""
        r1 = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        r2 = _make_rec("R2", "experience", "EXPERIENCE_PARTIAL_MATCH", 75)
        r3 = _make_rec("R3", "education", "EDUCATION_PARTIAL_MATCH", 50)
        orchestrated = _make_orchestrated(
            recs=(r1, r2, r3),
            high=(r1,),
            medium=(r2,),
            low=(r3,),
            by_section={"skill": (r1,), "experience": (r2,), "education": (r3,)},
            by_category={"SKILL_MISSING": (r1,), "EXPERIENCE_PARTIAL_MATCH": (r2,), "EDUCATION_PARTIAL_MATCH": (r3,)},
        )
        result = self.engine.process(orchestrated)

        self.assertEqual(3, result.total_recommendations)
        self.assertEqual(1, result.high_priority)
        self.assertEqual(1, result.medium_priority)
        self.assertEqual(1, result.low_priority)
        self.assertEqual(3, len(result.section_summaries))
        self.assertEqual(3, len(result.top_recommendations))

    def test_statistics_populated(self) -> None:
        """Statistics must be populated with correct counts."""
        rec = _make_rec("REC_1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(
            recs=(rec,),
            high=(rec,),
            by_section={"skill": (rec,)},
            by_category={"SKILL_MISSING": (rec,)},
        )
        result = self.engine.process(orchestrated)

        self.assertTrue(result.statistics.summary_generated)
        self.assertEqual(1, result.statistics.sections_processed)
        self.assertEqual(1, result.statistics.recommendations_processed)
        self.assertGreater(result.statistics.execution_time_ms, 0.0)

    def test_return_type_is_resume_intelligence_summary(self) -> None:
        """Return type must always be ResumeIntelligenceSummary."""
        orchestrated = _make_orchestrated()
        result = self.engine.process(orchestrated)
        self.assertIsInstance(result, ResumeIntelligenceSummary)


if __name__ == "__main__":
    unittest.main()
