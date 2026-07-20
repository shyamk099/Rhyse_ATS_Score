"""Shared test helpers and fixtures for orchestrator tests."""

from __future__ import annotations

from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary


def make_collection() -> CanonicalMatchCollection:
    """Return a minimal, valid CanonicalMatchCollection for tests."""
    return CanonicalMatchCollection(
        results=(),
        statistics=MatchStatistics(),
        validation_summary=ValidationSummary(),
    )


def make_scorer(name: str, raw_score: float = 10.0) -> type[AbstractScorer]:
    """Dynamically create a named stub scorer class."""

    class _StubScorer(AbstractScorer):
        def validate(self, context: ScoringContext) -> None:
            pass

        def score(self, context: ScoringContext) -> SectionScore:
            return SectionScore(section_name=name, raw_score=raw_score, maximum_score=100.0)

        def build(self, context: ScoringContext) -> SectionScore:
            return self.score(context)

        def statistics(self) -> dict:
            return {"processed": 1}

        def metadata(self) -> dict:
            return {"version": "1.0.0"}

    _StubScorer.__name__ = f"{name}Scorer"
    _StubScorer.__qualname__ = f"{name}Scorer"
    return _StubScorer


def make_failing_scorer(name: str) -> type[AbstractScorer]:
    """Dynamically create a scorer that raises on validate()."""

    class _FailScorer(AbstractScorer):
        def validate(self, context: ScoringContext) -> None:
            raise RuntimeError(f"Intentional failure in {name}")

        def score(self, context: ScoringContext) -> SectionScore:
            return SectionScore(section_name=name)

        def build(self, context: ScoringContext) -> SectionScore:
            return self.score(context)

        def statistics(self) -> dict:
            return {}

        def metadata(self) -> dict:
            return {}

    _FailScorer.__name__ = f"Failing{name}Scorer"
    _FailScorer.__qualname__ = f"Failing{name}Scorer"
    return _FailScorer
