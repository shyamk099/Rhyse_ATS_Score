"""Tests for ResumeSummaryValidator.

Purpose:
    Verify validator correctly detects conservation errors, subset violations,
    and duplicate ID violations.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.models import (
    OrchestratedRecommendationResult,
    OrchestrationStatistics,
)
from ats_engine.domain.recommendation.summary.models import (
    ResumeIntelligenceSummary,
    ResumeHealth,
    ResumeSectionSummary,
    ResumeIntelligenceStatistics,
)
from ats_engine.domain.recommendation.summary.summary_validator import ResumeSummaryValidator
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


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
    recs: tuple[Recommendation, ...],
    high: tuple[Recommendation, ...] = (),
    medium: tuple[Recommendation, ...] = (),
    low: tuple[Recommendation, ...] = (),
    by_section: dict | None = None,
) -> OrchestratedRecommendationResult:
    return OrchestratedRecommendationResult(
        recommendations=recs,
        grouped_recommendations={},
        recommendations_by_section=by_section or {},
        recommendations_by_priority={"High": high, "Medium": medium, "Low": low},
        statistics=OrchestrationStatistics(
            execution_time_ms=0.1,
            recommendations_processed=len(recs),
            sections=0,
            categories=0,
            high_priority=len(high),
            medium_priority=len(medium),
            low_priority=len(low),
            largest_section="",
            largest_category="",
            success=True,
        ),
        total_recommendations=len(recs),
    )


def _make_stats() -> ResumeIntelligenceStatistics:
    return ResumeIntelligenceStatistics(
        execution_time_ms=0.1,
        sections_processed=1,
        recommendations_processed=1,
        summary_generated=True,
    )


class SummaryValidatorTests(unittest.TestCase):
    """Test suite validating ResumeSummaryValidator constraints."""

    def test_valid_summary_passes(self) -> None:
        """A correctly constructed summary must pass validation."""
        rec = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(
            recs=(rec,), high=(rec,), by_section={"skill": (rec,)},
        )
        summary = ResumeIntelligenceSummary(
            overall_health=ResumeHealth(score=85.0, grade="B", status="Good"),
            total_recommendations=1,
            high_priority=1,
            medium_priority=0,
            low_priority=0,
            section_summaries=(
                ResumeSectionSummary(section="skill", total_recommendations=1, high_priority=1, medium_priority=0, low_priority=0),
            ),
            top_recommendations=(rec,),
            statistics=_make_stats(),
        )
        # Should not raise
        ResumeSummaryValidator.validate(summary, orchestrated)

    def test_total_mismatch_raises(self) -> None:
        """A total count mismatch must raise validation error."""
        rec = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(recs=(rec,), high=(rec,), by_section={"skill": (rec,)})
        summary = ResumeIntelligenceSummary(
            overall_health=ResumeHealth(score=85.0, grade="B", status="Good"),
            total_recommendations=2,  # wrong
            high_priority=2,
            medium_priority=0,
            low_priority=0,
            section_summaries=(
                ResumeSectionSummary(section="skill", total_recommendations=2, high_priority=2, medium_priority=0, low_priority=0),
            ),
            top_recommendations=(rec,),
            statistics=_make_stats(),
        )
        with self.assertRaises(RecommendationValidationError):
            ResumeSummaryValidator.validate(summary, orchestrated)

    def test_priority_mismatch_raises(self) -> None:
        """A high-priority count mismatch must raise validation error."""
        rec = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(recs=(rec,), high=(rec,), by_section={"skill": (rec,)})
        summary = ResumeIntelligenceSummary(
            overall_health=ResumeHealth(score=85.0, grade="B", status="Good"),
            total_recommendations=1,
            high_priority=0,  # mismatch
            medium_priority=1,
            low_priority=0,
            section_summaries=(
                ResumeSectionSummary(section="skill", total_recommendations=1, high_priority=0, medium_priority=1, low_priority=0),
            ),
            top_recommendations=(rec,),
            statistics=_make_stats(),
        )
        with self.assertRaises(RecommendationValidationError):
            ResumeSummaryValidator.validate(summary, orchestrated)

    def test_section_total_mismatch_raises(self) -> None:
        """Section totals not summing to overall total must raise."""
        rec = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(recs=(rec,), high=(rec,), by_section={"skill": (rec,)})
        summary = ResumeIntelligenceSummary(
            overall_health=ResumeHealth(score=85.0, grade="B", status="Good"),
            total_recommendations=1,
            high_priority=1,
            medium_priority=0,
            low_priority=0,
            section_summaries=(),  # empty — sums to 0, not 1
            top_recommendations=(rec,),
            statistics=_make_stats(),
        )
        with self.assertRaises(RecommendationValidationError):
            ResumeSummaryValidator.validate(summary, orchestrated)

    def test_top_recommendation_not_in_main_raises(self) -> None:
        """A top recommendation not in the main list must raise."""
        rec = _make_rec("R1", "skill", "SKILL_MISSING", 100)
        orphan = _make_rec("ORPHAN", "skill", "SKILL_MISSING", 100)
        orchestrated = _make_orchestrated(recs=(rec,), high=(rec,), by_section={"skill": (rec,)})
        summary = ResumeIntelligenceSummary(
            overall_health=ResumeHealth(score=85.0, grade="B", status="Good"),
            total_recommendations=1,
            high_priority=1,
            medium_priority=0,
            low_priority=0,
            section_summaries=(
                ResumeSectionSummary(section="skill", total_recommendations=1, high_priority=1, medium_priority=0, low_priority=0),
            ),
            top_recommendations=(orphan,),
            statistics=_make_stats(),
        )
        with self.assertRaises(RecommendationValidationError):
            ResumeSummaryValidator.validate(summary, orchestrated)


if __name__ == "__main__":
    unittest.main()
