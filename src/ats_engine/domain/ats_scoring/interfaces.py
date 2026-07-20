"""Scoring Engine Abstract Interface.

Purpose:
    Define AbstractScorer from which every concrete section scorer must inherit.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Sequence
from enum import Enum

from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.matching.models import MatchResult


class AbstractScorer(ABC):
    """Abstract interface defining required hooks for validating and scoring matches."""

    @abstractmethod
    def validate(self, context: ScoringContext) -> None:
        """Validate input features or matches within scoring context."""

    @abstractmethod
    def score(self, context: ScoringContext) -> SectionScore:
        """Run calculations (deferred to later milestones) and return SectionScore."""

    @abstractmethod
    def build(self, context: ScoringContext) -> SectionScore:
        """Assemble finalized SectionScore containing statistics and telemetry."""

    @abstractmethod
    def statistics(self) -> dict[str, Any]:
        """Expose current scoring telemetry/stats counts."""

    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """Expose current scorer version metadata."""


class BaseSectionScorer(AbstractScorer, ABC):
    """Abstract base class for section scorers providing standard telemetry properties."""

    def __init__(self) -> None:
        """Initialize telemetry statistics and metadata dictionary fields."""
        self._stats: dict[str, Any] = {}
        self._metadata: dict[str, Any] = {}

    def statistics(self) -> dict[str, Any]:
        """Expose current execution statistics dictionary."""
        return self._stats

    def metadata(self) -> dict[str, Any]:
        """Expose current scorer metadata dictionary."""
        return self._metadata


TClassification = TypeVar("TClassification", bound=Enum)


class AbstractClassificationResolver(Generic[TClassification], ABC):
    """Abstract base interface for resolving domain classifications from MatchResult metadata."""

    @abstractmethod
    def resolve(self, result: MatchResult) -> TClassification:
        """Translate a MatchResult to an internal domain classification Enum."""

    @abstractmethod
    def validate(self, result: MatchResult) -> None:
        """Verify classification constraints on the match result."""

    @abstractmethod
    def supported_classifications(self) -> Sequence[str]:
        """Expose sequence of supported classification values."""


