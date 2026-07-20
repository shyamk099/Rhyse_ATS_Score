"""OverallScoreAggregator definition.

Purpose:
    Consume an immutable ScoreResult from the ScoreOrchestrator, normalize
    section scores, apply weights, compute the final ATS score, and return
    a new ScoreResult with overall_score populated.

The aggregator NEVER:
    - Executes any scorer
    - Inspects MatchResults
    - Modifies SectionScore objects
    - Applies penalties, bonuses, or business logic
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.aggregation.normalization import ScoreNormalizer
from ats_engine.domain.ats_scoring.aggregation.validator import AggregationValidator
from ats_engine.domain.ats_scoring.aggregation.statistics_builder import AggregationStatisticsBuilder
from ats_engine.domain.ats_scoring.exceptions import AggregationError
from ats_engine.infrastructure.logging.factory import LoggerFactory


class OverallScoreAggregator:
    """Computes the overall ATS score from a fully populated ScoreResult.

    Aggregation formula:
        overall = (
            normalized_skill         × weight.skill         +
            normalized_experience    × weight.experience    +
            normalized_education     × weight.education     +
            normalized_project       × weight.project       +
            normalized_certification × weight.certification
        )
        overall = clamp(overall, 0.0, 100.0)

    Result is returned as a new ScoreResult (via model_copy) with overall_score
    set to the computed value. The original ScoreResult is never mutated.
    """

    AGGREGATOR_VERSION: str = "1.0.0"

    def __init__(
        self,
        weight_config: SectionWeightConfiguration | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the aggregator with an optional weight configuration.

        Args:
            weight_config: Weight configuration; defaults to standard weights if None.
            logger: Optional logger; defaults to module-level logger.
        """
        self._weight_config = weight_config or SectionWeightConfiguration()
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._last_aggregation_stats: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def weight_config(self) -> SectionWeightConfiguration:
        """Return the active SectionWeightConfiguration."""
        return self._weight_config

    @property
    def last_aggregation_stats(self) -> dict[str, Any]:
        """Return statistics from the most recent aggregate() call."""
        return dict(self._last_aggregation_stats)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def aggregate(self, score_result: ScoreResult) -> ScoreResult:
        """Compute overall_score and return a new ScoreResult with it populated.

        Execution lifecycle:
            1. AggregationValidator.validate()
            2. ScoreNormalizer.normalize_all()  → dict[section → float]
            3. Weighted average → overall_score
            4. Clamp to [0.0, 100.0]
            5. score_result.model_copy(update={"overall_score": overall})
            6. Return new ScoreResult

        Args:
            score_result: The ScoreResult produced by ScoreOrchestrator.orchestrate().

        Returns:
            A new immutable ScoreResult with overall_score populated.

        Raises:
            AggregationValidationError: If the ScoreResult fails structural validation.
            NormalizationError: If any section cannot be normalized.
            AggregationError: If an unexpected aggregation failure occurs.
        """
        aggregation_start = time.perf_counter()

        # Step 1 — Pre-aggregation validation
        try:
            AggregationValidator.validate(score_result, self._weight_config)
        except Exception:
            self._logger.exception("aggregation_validation_failed")
            raise

        # Step 2 — Normalize all sections
        norm_start = time.perf_counter()
        try:
            normalized = ScoreNormalizer.normalize_all(score_result)
        except Exception:
            self._logger.exception("aggregation_normalization_failed")
            raise
        norm_time_ms = (time.perf_counter() - norm_start) * 1000.0

        # Step 3 — Apply weights
        weight_start = time.perf_counter()
        try:
            overall = self._compute_weighted_average(normalized)
        except Exception as exc:
            self._logger.exception("aggregation_weighting_failed")
            raise AggregationError(f"Weighted average computation failed: {exc}") from exc
        weight_time_ms = (time.perf_counter() - weight_start) * 1000.0

        # Step 4 — Clamp
        overall = max(0.0, min(100.0, overall))

        aggregation_time_ms = (time.perf_counter() - aggregation_start) * 1000.0

        # Step 5 — Compile statistics
        self._last_aggregation_stats = AggregationStatisticsBuilder.build(
            aggregation_time_ms=aggregation_time_ms,
            normalization_time_ms=norm_time_ms,
            weighting_time_ms=weight_time_ms,
            overall_score=overall,
            pipeline_version=score_result.metadata.pipeline_version,
            aggregation_version=self.AGGREGATOR_VERSION,
        )

        self._logger.debug(
            "aggregation_complete",
            extra={
                "overall_score": overall,
                "normalized_sections": normalized,
                "aggregation_time_ms": aggregation_time_ms,
            },
        )

        # Step 6 — Return new ScoreResult with overall_score populated (Option A)
        return score_result.model_copy(update={"overall_score": overall})

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _compute_weighted_average(self, normalized: dict[str, float]) -> float:
        """Apply section weights to normalized scores and return the overall value.

        Args:
            normalized: Dict mapping section name → normalized float [0.0, 100.0].

        Returns:
            The weighted sum as a float (before clamping).
        """
        weights = self._weight_config
        return (
            normalized["SKILL"]         * weights.skill         +
            normalized["EXPERIENCE"]    * weights.experience    +
            normalized["EDUCATION"]     * weights.education     +
            normalized["PROJECT"]       * weights.project       +
            normalized["CERTIFICATION"] * weights.certification
        )
