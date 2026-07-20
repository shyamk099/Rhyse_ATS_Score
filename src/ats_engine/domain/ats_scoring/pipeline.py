"""ScoringPipeline definition.

Purpose:
    Sequence validation, dynamic resolution of scorers from registry, priority execution,
    and compilation of final ScoreResult.
"""

from __future__ import annotations

import logging
import time

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.common.validator import ScoreValidator
from ats_engine.domain.ats_scoring.common.builder import ScoringContextBuilder
from ats_engine.domain.ats_scoring.common.statistics_builder import ScoreStatisticsBuilder
from ats_engine.domain.ats_scoring.common.metadata_builder import ScoreMetadataBuilder
from ats_engine.domain.ats_scoring.exceptions import ScoringPipelineError
from ats_engine.domain.ats_scoring.constants import SKILL, EXPERIENCE, EDUCATION, PROJECT, CERTIFICATION
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ScoringPipeline:
    """Orchestrates execution of the scoring process across registered segment scorers."""

    def __init__(
        self,
        registry: ScoringRegistry,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize pipeline with injected scorer registry."""
        self._registry = registry
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def execute(
        self,
        match_collection: CanonicalMatchCollection,
        rules: ScoringRules,
    ) -> ScoreResult:
        """Execute active scorers, compile telemetry and return ScoreResult.

        Raises:
            ScoringPipelineError: Under STRICT strictness or on validation failures.
        """
        start_time = time.perf_counter()

        # 1. Validation
        try:
            ScoreValidator.validate(match_collection, rules)
        except Exception as exc:
            self._logger.exception("scoring_pipeline_validation_failed")
            raise ScoringPipelineError(f"Scoring pipeline validation failed: {exc}") from exc

        # 2. Context assembly
        context = ScoringContextBuilder.build(match_collection, rules)

        # 3. Resolve active scorers ordered by priority
        registered_names = self._registry.list()
        scorer_configs = []
        executed_scorers: list[str] = []
        skipped_scorers: list[str] = []
        failed_scorers: list[str] = []
        warnings: list[str] = []
        validation_errors: list[str] = []

        for name in registered_names:
            try:
                meta = self._registry.get_metadata(name)
                scorer_cls = self._registry.get(name)
                scorer_configs.append({
                    "name": name,
                    "scorer_cls": scorer_cls,
                    "priority": meta.get("priority", 100),
                    "enabled": meta.get("enabled", True),
                })
            except Exception as exc:
                self._logger.error(
                    "scoring_pipeline_resolve_failed",
                    extra={"scorer_name": name, "error": str(exc)},
                )
                failed_scorers.append(name)
                validation_errors.append(f"Failed to resolve scorer '{name}': {exc}")

        # Sort priority descending: highest priority executes first
        scorer_configs.sort(key=lambda x: x["priority"], reverse=True)

        section_scores: dict[str, SectionScore] = {}

        # 4. Sequentially execute scorers
        for cfg in scorer_configs:
            name = cfg["name"]
            if not cfg["enabled"]:
                skipped_scorers.append(name)
                continue

            scorer_cls = cfg["scorer_cls"]
            try:
                scorer_inst = scorer_cls()

                # Validate, score, and build hooks execution
                scorer_inst.validate(context)
                sec_score = scorer_inst.score(context)

                if not isinstance(sec_score, SectionScore):
                    sec_score = SectionScore(section_name=name)

                section_scores[name] = sec_score
                executed_scorers.append(name)
            except Exception as exc:
                self._logger.exception(
                    "scoring_pipeline_scorer_failed",
                    extra={"scorer_name": name, "error": str(exc)},
                )
                failed_scorers.append(name)
                if rules.strictness == "STRICT":
                    raise ScoringPipelineError(
                        f"Scorer '{name}' failed under STRICT rules: {exc}"
                    ) from exc
                else:
                    warnings.append(f"Scorer '{name}' execution failed: {exc}")

        # Ensure placeholders exist for all supported categories if not processed
        for cat in [SKILL, EXPERIENCE, EDUCATION, PROJECT, CERTIFICATION]:
            if cat not in section_scores:
                section_scores[cat] = SectionScore(section_name=cat)

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0

        # 5. Compile telemetry
        stats = ScoreStatisticsBuilder.build(
            total_sections=len(section_scores),
            registered_scorers=registered_names,
            executed_scorers=executed_scorers,
            skipped_scorers=skipped_scorers,
            failed_scorers=failed_scorers,
            warnings=warnings,
            validation_errors=validation_errors,
            processing_time_ms=processing_time_ms,
        )

        metadata = ScoreMetadataBuilder.build(
            rules_version=rules.version,
            processing_time_ms=processing_time_ms,
        )

        # 6. Return ScoreResult
        return ScoreResult(
            overall_score=None,
            skill_score=section_scores[SKILL],
            experience_score=section_scores[EXPERIENCE],
            education_score=section_scores[EDUCATION],
            project_score=section_scores[PROJECT],
            certification_score=section_scores[CERTIFICATION],
            statistics=stats,
            metadata=metadata,
            warnings=tuple(warnings),
            validation_summary={"status": "VALID" if not failed_scorers else "INVALID"},
        )
