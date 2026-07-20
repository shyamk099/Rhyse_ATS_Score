"""ScoringService coordination facade.

Purpose:
    Provide the public API entry point for executing match collection scoring runs.
"""

from __future__ import annotations

import logging

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ScoringService:
    """Public service boundary coordinating pipeline invocations for scoring runs."""

    def __init__(
        self,
        registry: ScoringRegistry | None = None,
        pipeline: ScoringPipeline | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize registry, pipeline, and logger instances."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._registry = registry or ScoringFactory.create_default_registry()
        self._pipeline = pipeline or ScoringFactory.create_default_pipeline(self._registry)

    @property
    def registry(self) -> ScoringRegistry:
        """Return the active ScoringRegistry associated with the service."""
        return self._registry

    def score(
        self,
        match_collection: CanonicalMatchCollection,
        rules: ScoringRules | None = None,
    ) -> ScoreResult:
        """Execute scoring pipeline on the given match collection.

        Args:
            match_collection: The verified CanonicalMatchCollection DTO.
            rules: The rules configuration. Fallbacks to default if None.

        Returns:
            The compiled, immutable ScoreResult DTO.
        """
        active_rules = rules or ScoringFactory.create_default_rules()
        return self._pipeline.execute(match_collection, active_rules)

