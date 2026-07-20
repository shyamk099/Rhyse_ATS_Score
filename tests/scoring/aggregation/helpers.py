"""Shared test helpers and fixtures for aggregation tests."""

from __future__ import annotations

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration


def make_metadata() -> ScoreMetadata:
    """Return a minimal, valid ScoreMetadata for tests."""
    return ScoreMetadata(
        engine_version="1.0.0",
        rules_version="1.0.0",
        generated_at="2026-01-01T00:00:00Z",
        processing_time_ms=0.0,
        pipeline_version="1.0.0",
        book_version="6",
        milestone="6.8",
    )


def make_statistics() -> ScoreStatistics:
    """Return a minimal, valid ScoreStatistics for tests."""
    return ScoreStatistics(
        total_sections=5,
        registered_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
        executed_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
    )


def make_section(
    name: str,
    raw_score: float = 10.0,
    maximum_score: float = 20.0,
) -> SectionScore:
    """Return a SectionScore with configurable raw and maximum scores."""
    return SectionScore(
        section_name=name,
        raw_score=raw_score,
        maximum_score=maximum_score,
    )


def make_score_result(
    skill_raw: float = 10.0,
    skill_max: float = 20.0,
    experience_raw: float = 15.0,
    experience_max: float = 25.0,
    education_raw: float = 9.0,
    education_max: float = 15.0,
    project_raw: float = 8.0,
    project_max: float = 15.0,
    certification_raw: float = 6.0,
    certification_max: float = 10.0,
) -> ScoreResult:
    """Return a fully populated ScoreResult for aggregation tests."""
    return ScoreResult(
        overall_score=None,
        skill_score=make_section("SKILL", skill_raw, skill_max),
        experience_score=make_section("EXPERIENCE", experience_raw, experience_max),
        education_score=make_section("EDUCATION", education_raw, education_max),
        project_score=make_section("PROJECT", project_raw, project_max),
        certification_score=make_section("CERTIFICATION", certification_raw, certification_max),
        statistics=make_statistics(),
        metadata=make_metadata(),
    )


def make_perfect_score_result() -> ScoreResult:
    """Return a ScoreResult where every section achieves its maximum score."""
    return make_score_result(
        skill_raw=40.0, skill_max=40.0,
        experience_raw=25.0, experience_max=25.0,
        education_raw=15.0, education_max=15.0,
        project_raw=15.0, project_max=15.0,
        certification_raw=10.0, certification_max=10.0,
    )


def make_zero_score_result() -> ScoreResult:
    """Return a ScoreResult where every section scores zero (raw=0)."""
    return make_score_result(
        skill_raw=0.0, skill_max=40.0,
        experience_raw=0.0, experience_max=25.0,
        education_raw=0.0, education_max=15.0,
        project_raw=0.0, project_max=15.0,
        certification_raw=0.0, certification_max=10.0,
    )


def make_default_weights() -> SectionWeightConfiguration:
    """Return the default SectionWeightConfiguration."""
    return SectionWeightConfiguration()
