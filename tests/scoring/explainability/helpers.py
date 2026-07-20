"""Shared test helpers and fixtures for explainability tests."""

from __future__ import annotations

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata


def make_metadata() -> ScoreMetadata:
    """Return a minimal, valid ScoreMetadata for tests."""
    return ScoreMetadata(
        engine_version="1.0.0",
        rules_version="1.0.0",
        generated_at="2026-01-01T00:00:00Z",
        processing_time_ms=0.0,
        pipeline_version="1.0.0",
        book_version="6",
        milestone="6.9",
    )


def make_statistics() -> ScoreStatistics:
    """Return a minimal, valid ScoreStatistics for tests."""
    return ScoreStatistics(
        total_sections=5,
        registered_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
        executed_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
    )


def make_breakdown(
    matched: tuple[str, ...] = ("python", "git"),
    missing: tuple[str, ...] = ("docker",),
    counts: dict[str, int] | None = None,
    raw_points: float = 17.0,
    max_points: float = 20.0,
) -> ScoreBreakdown:
    """Return a ScoreBreakdown DTO."""
    return ScoreBreakdown(
        matched_items=matched,
        missing_items=missing,
        classification_counts=counts or {"mandatory": 2, "optional": 1},
        raw_points=raw_points,
        maximum_points=max_points,
        rules_version="1.0.0",
    )


def make_section(
    name: str,
    raw_score: float = 17.0,
    maximum_score: float = 20.0,
    breakdown: ScoreBreakdown | None = None,
) -> SectionScore:
    """Return a SectionScore with configurable scores and breakdown."""
    return SectionScore(
        section_name=name,
        raw_score=raw_score,
        maximum_score=maximum_score,
        breakdown=breakdown or make_breakdown(
            raw_points=raw_score if raw_score is not None else 0.0,
            max_points=maximum_score if maximum_score is not None else 0.0
        ),
    )


def make_score_result(
    overall_score: float | None = 82.40,
    skill_raw: float = 17.0,
    skill_max: float = 20.0,
    experience_raw: float = 19.0,
    experience_max: float = 25.0,
    education_raw: float = 15.0,
    education_max: float = 15.0,
    project_raw: float = 6.9,
    project_max: float = 10.0,
    certification_raw: float = 7.95,
    certification_max: float = 10.0,
) -> ScoreResult:
    """Return a fully populated ScoreResult for explainability tests."""
    return ScoreResult(
        overall_score=overall_score,
        skill_score=make_section("SKILL", skill_raw, skill_max),
        experience_score=make_section("EXPERIENCE", experience_raw, experience_max),
        education_score=make_section("EDUCATION", education_raw, education_max),
        project_score=make_section("PROJECT", project_raw, project_max),
        certification_score=make_section("CERTIFICATION", certification_raw, certification_max),
        statistics=make_statistics(),
        metadata=make_metadata(),
    )


def make_perfect_score_result() -> ScoreResult:
    """Return a ScoreResult where every section has maximum points."""
    return make_score_result(
        overall_score=100.00,
        skill_raw=40.0, skill_max=40.0,
        experience_raw=25.0, experience_max=25.0,
        education_raw=15.0, education_max=15.0,
        project_raw=15.0, project_max=15.0,
        certification_raw=10.0, certification_max=10.0,
    )


def make_zero_score_result() -> ScoreResult:
    """Return a ScoreResult where every section has 0 raw points."""
    return make_score_result(
        overall_score=0.00,
        skill_raw=0.0, skill_max=40.0,
        experience_raw=0.0, experience_max=25.0,
        education_raw=0.0, education_max=15.0,
        project_raw=0.0, project_max=15.0,
        certification_raw=0.0, certification_max=10.0,
    )
