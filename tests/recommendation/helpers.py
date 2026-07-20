"""Shared test helpers and mock classes for recommendation tests."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult, SectionExplanation, OverallExplanation
from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider
from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class DummyProvider(BaseRecommendationProvider):
    """A dummy recommendation provider for testing the framework."""

    def __init__(
        self,
        name: str = "DUMMY_PROVIDER",
        priority_val: int = 10,
        recommendations_to_generate: tuple[Recommendation, ...] = (),
        should_fail_validation: bool = False,
        should_fail_generate: bool = False,
    ) -> None:
        self._name = name
        self._priority = priority_val
        self._recs = recommendations_to_generate
        self._should_fail_validation = should_fail_validation
        self._should_fail_generate = should_fail_generate
        self.validate_called = 0
        self.generate_called = 0

    def provider_name(self) -> str:
        return self._name

    def priority(self) -> int:
        return self._priority

    def validate(self, context: RecommendationContext) -> None:
        self.validate_called += 1
        if self._should_fail_validation:
            from ats_engine.domain.recommendation.exceptions import RecommendationProviderError
            raise RecommendationProviderError(f"Validation failed for provider {self._name}")

    def generate(self, context: RecommendationContext) -> tuple[Recommendation, ...]:
        self.generate_called += 1
        if self._should_fail_generate:
            raise RuntimeError("Unexpected failure during generation")
        return self._recs


def make_dummy_recommendation(
    rec_id: str = "REC_001",
    section: str = "SKILL",
    category: str = "missing_skill",
    priority: int = 1,
    title: str = "Add Docker Skill",
    description: str = "Resume is missing Docker experience.",
    impact: float = 5.0,
) -> Recommendation:
    """Return a single Recommendation DTO."""
    return Recommendation(
        recommendation_id=rec_id,
        section=section,
        category=category,
        priority=priority,
        title=title,
        description=description,
        impact=impact,
        metadata={"provenance": "test"},
    )


def make_mock_match_collection() -> CanonicalMatchCollection:
    """Return a minimal valid CanonicalMatchCollection."""
    return CanonicalMatchCollection(
        results=(),
        statistics=MatchStatistics(
            total_resume_features=0,
            total_job_features=0,
            total_matches=0,
            duplicate_count=0,
            validation_error_count=0,
            warning_count=0,
            category_counts={},
            execution_duration_ms=0.0,
        ),
        validation_summary=ValidationSummary(
            errors=(),
            warnings=(),
            total_errors=0,
            total_warnings=0,
        ),
    )


def make_mock_score_result(overall_score: float | None = 85.0) -> ScoreResult:
    """Return a minimal valid ScoreResult."""
    return ScoreResult(
        overall_score=overall_score,
        skill_score=SectionScore(section_name="SKILL", raw_score=10.0, maximum_score=20.0),
        experience_score=SectionScore(section_name="EXPERIENCE", raw_score=15.0, maximum_score=20.0),
        education_score=SectionScore(section_name="EDUCATION", raw_score=5.0, maximum_score=10.0),
        project_score=SectionScore(section_name="PROJECT", raw_score=8.0, maximum_score=10.0),
        certification_score=SectionScore(section_name="CERTIFICATION", raw_score=9.0, maximum_score=10.0),
        statistics=ScoreStatistics(
            total_sections=5,
            registered_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
            executed_scorers=("SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"),
        ),
        metadata=ScoreMetadata(
            engine_version="1.0.0",
            rules_version="1.0.0",
            generated_at="2026-01-01T00:00:00Z",
            processing_time_ms=0.0,
            pipeline_version="1.0.0",
            book_version="6",
            milestone="6.8",
        ),
    )


def make_mock_explainability_result(score_result: ScoreResult) -> ExplainabilityResult:
    """Return a minimal valid ExplainabilityResult wrapping a ScoreResult."""
    overall_exp = None
    if score_result.overall_score is not None:
        overall_exp = OverallExplanation(
            overall_score=score_result.overall_score,
            formula="...",
            section_contributions={},
            weight_configuration_version="1.0.0",
            summary="...",
        )
    return ExplainabilityResult(
        score_result=score_result,
        overall_explanation=overall_exp,
        section_explanations={
            "SKILL": SectionExplanation(
                section_name="SKILL",
                raw_score=10.0,
                maximum_score=20.0,
                normalized_score=50.0,
                weight_used=0.35,
                formula="...",
                summary="...",
            )
        },
        statistics={},
        metadata={"explainability_version": "1.0.0"},
    )


def make_recommendation_context(
    match_collection: CanonicalMatchCollection | None = None,
    score_result: ScoreResult | None = None,
    explainability_result: ExplainabilityResult | None = None,
) -> RecommendationContext:
    """Helper to compile a valid RecommendationContext."""
    mc = match_collection or make_mock_match_collection()
    sr = score_result or make_mock_score_result()
    er = explainability_result or make_mock_explainability_result(sr)
    return RecommendationContext(
        match_collection=mc,
        score_result=sr,
        explainability_result=er,
    )

