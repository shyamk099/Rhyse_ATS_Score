"""ScoreOrchestrator definition.

Purpose:
    Coordinate all section scorers through the ScoringPipeline,
    producing an immutable ScoreResult without implementing scoring logic.

Lifecycle:
    1. ScoreOrchestratorValidator.validate()   — pre-flight registry checks
    2. ExecutionPlan.build()                   — deterministic planning step
    3. ScoringPipeline.execute()               — delegate all scoring
    4. OrchestratorStatisticsBuilder.build()   — wrap wall-clock stats
    5. Return ScoreResult (unmodified from pipeline)
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan
from ats_engine.domain.ats_scoring.orchestrator.validator import ScoreOrchestratorValidator
from ats_engine.domain.ats_scoring.orchestrator.statistics_builder import OrchestratorStatisticsBuilder
from ats_engine.domain.ats_scoring.exceptions import OrchestrationError, ExecutionPlanError, RegistryValidationError
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ScoreOrchestrator:
    """Coordination layer that produces a complete, immutable ScoreResult.

    Responsibilities:
        - Run pre-flight registry validation.
        - Build an ExecutionPlan (isolated planning step).
        - Delegate scoring to the ScoringPipeline.
        - Capture wall-clock orchestration statistics.
        - Return the pipeline's ScoreResult unmodified.

    The orchestrator NEVER calculates scores. All scoring is delegated
    to the ScoringPipeline and the registered section scorers.
    """

    ORCHESTRATOR_VERSION: str = "1.0.0"

    def __init__(
        self,
        pipeline: ScoringPipeline,
        registry: ScoringRegistry,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the orchestrator with an injected pipeline and registry.

        Args:
            pipeline: The ScoringPipeline that executes section scorers.
            registry: The ScoringRegistry used to build the ExecutionPlan.
            logger: Optional logger; defaults to module-level logger.
        """
        self._pipeline = pipeline
        self._registry = registry
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._last_orchestration_stats: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def pipeline(self) -> ScoringPipeline:
        """Return the injected ScoringPipeline."""
        return self._pipeline

    @property
    def registry(self) -> ScoringRegistry:
        """Return the injected ScoringRegistry."""
        return self._registry

    @property
    def last_orchestration_stats(self) -> dict[str, Any]:
        """Return the statistics dict from the most recent orchestrate() call."""
        return dict(self._last_orchestration_stats)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def orchestrate(
        self,
        match_collection: CanonicalMatchCollection,
        rules: ScoringRules | None = None,
    ) -> ScoreResult:
        """Coordinate all section scorers and return an immutable ScoreResult.

        Execution lifecycle:
            1. Pre-flight registry validation (raises RegistryValidationError on failure).
            2. ExecutionPlan construction (raises ExecutionPlanError on failure).
            3. Delegate to ScoringPipeline.execute() — all scoring occurs here.
            4. Compile orchestration statistics.
            5. Return the ScoreResult produced by the pipeline (unmodified).

        Args:
            match_collection: The CanonicalMatchCollection to score.
            rules: ScoringRules configuration; falls back to default if None.

        Returns:
            The immutable ScoreResult produced by the pipeline.

        Raises:
            RegistryValidationError: If the registry fails pre-flight validation.
            ExecutionPlanError: If the execution plan cannot be constructed.
            OrchestrationError: If an unexpected orchestration failure occurs.
        """
        active_rules = rules or ScoringRules()
        orchestration_start = time.perf_counter()

        # Step 1 — Pre-flight validation
        try:
            ScoreOrchestratorValidator.validate(self._registry)
        except RegistryValidationError:
            self._logger.exception("orchestration_registry_validation_failed")
            raise

        # Step 2 — Build execution plan (planning only; no execution)
        try:
            plan = ExecutionPlan.build(self._registry)
        except ExecutionPlanError:
            self._logger.exception("orchestration_execution_plan_failed")
            raise

        self._logger.debug(
            "orchestration_plan_built",
            extra={
                "execution_order": plan.execution_order,
                "skipped": plan.skipped,
            },
        )

        # Step 3 — Delegate all scoring to the pipeline
        try:
            result: ScoreResult = self._pipeline.execute(match_collection, active_rules)
        except Exception as exc:
            orchestration_time_ms = (time.perf_counter() - orchestration_start) * 1000.0
            self._last_orchestration_stats = OrchestratorStatisticsBuilder.build(
                execution_time_ms=orchestration_time_ms,
                sections_executed=(),
                sections_skipped=plan.skipped,
                failed_sections=plan.execution_order,
                pipeline_version=self.ORCHESTRATOR_VERSION,
                success=False,
            )
            self._logger.exception(
                "orchestration_pipeline_execution_failed",
                extra={"error": str(exc)},
            )
            raise OrchestrationError(
                f"Pipeline execution failed during orchestration: {exc}"
            ) from exc

        orchestration_time_ms = (time.perf_counter() - orchestration_start) * 1000.0

        # Step 4 — Compile orchestration-level statistics
        executed = tuple(result.statistics.executed_scorers)
        skipped = tuple(result.statistics.skipped_scorers)
        failed = tuple(result.statistics.failed_scorers)

        self._last_orchestration_stats = OrchestratorStatisticsBuilder.build(
            execution_time_ms=orchestration_time_ms,
            section_execution_times=self._extract_section_times(result),
            sections_executed=executed,
            sections_skipped=skipped,
            failed_sections=failed,
            pipeline_version=self.ORCHESTRATOR_VERSION,
            success=len(failed) == 0,
        )

        self._logger.debug(
            "orchestration_complete",
            extra={
                "execution_time_ms": orchestration_time_ms,
                "sections_executed": executed,
                "sections_skipped": skipped,
                "failed_sections": failed,
            },
        )

        # Step 5 — Return the pipeline's ScoreResult unmodified
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _extract_section_times(self, result: ScoreResult) -> dict[str, float]:
        """Extract per-section execution times from each SectionScore's metadata.

        Falls back to an empty dict if metadata is not present or not populated.
        """
        times: dict[str, float] = {}
        sections = {
            "SKILL": result.skill_score,
            "EXPERIENCE": result.experience_score,
            "EDUCATION": result.education_score,
            "PROJECT": result.project_score,
            "CERTIFICATION": result.certification_score,
        }
        for section_name, section_score in sections.items():
            if section_score is not None and isinstance(section_score.metadata, dict):
                elapsed = section_score.metadata.get("processing_time_ms")
                if isinstance(elapsed, (int, float)):
                    times[section_name] = float(elapsed)
        return times
