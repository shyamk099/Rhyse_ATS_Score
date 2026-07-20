"""ExplainabilityEngine implementation.

Purpose:
    Expose score explainability coordination that parses ScoreResult section scores
    and returns a structured, immutable ExplainabilityResult.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.explainability.models import (
    SectionExplanation,
    OverallExplanation,
    ExplainabilityResult,
)
from ats_engine.domain.ats_scoring.explainability.formatter import ExplainabilityFormatter
from ats_engine.domain.ats_scoring.explainability.metadata_builder import ExplainabilityMetadataBuilder
from ats_engine.domain.ats_scoring.explainability.statistics_builder import ExplainabilityStatisticsBuilder
from ats_engine.domain.ats_scoring.exceptions import (
    ExplainabilityError,
    ExplainabilityValidationError,
)
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ExplainabilityEngine:
    """Deterministic score explainability coordinator.

    Produces SectionExplanation DTOs and optionally OverallExplanation DTO,
    wrapping them in a final immutable ExplainabilityResult.
    """

    EXPLAINER_VERSION: str = "1.0.0"

    def __init__(
        self,
        weight_config: SectionWeightConfiguration | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the engine with an optional weight configuration.

        Args:
            weight_config: Section weights. Defaults to standard configuration if None.
            logger: Optional Logger.
        """
        self._weight_config = weight_config or SectionWeightConfiguration()
        self._logger = logger or LoggerFactory.get_logger(__name__)

    @property
    def weight_config(self) -> SectionWeightConfiguration:
        """Return the active SectionWeightConfiguration."""
        return self._weight_config

    def explain(self, score_result: ScoreResult) -> ExplainabilityResult:
        """Analyze scores and generate explainability outputs.

        Args:
            score_result: The ScoreResult to explain.

        Returns:
            An immutable ExplainabilityResult enclosing all explanations and telemetry.

        Raises:
            ExplainabilityValidationError: If the input result fails validation checks.
            ExplainabilityError: If any processing error occurs.
        """
        start_time = time.perf_counter()

        # Step 1: Validation
        self._validate_input(score_result)

        sections_processed: list[str] = []
        section_explanations: dict[str, SectionExplanation] = {}
        section_contributions: dict[str, float] = {}

        formula_gen_time = 0.0
        formatting_time = 0.0

        # Mappings of DTO attributes to section names
        section_mappings = {
            "skill_score": "SKILL",
            "experience_score": "EXPERIENCE",
            "education_score": "EDUCATION",
            "project_score": "PROJECT",
            "certification_score": "CERTIFICATION",
        }

        # Step 2: Explain individual sections
        for attr, name in section_mappings.items():
            section = getattr(score_result, attr)
            sections_processed.append(name)

            # Get weight
            weight = getattr(self._weight_config, name.lower())

            # Perform raw contribution calculation
            # contribution = normalized_score * weight
            # normalized_score = (raw / maximum) * 100
            norm = (section.raw_score / section.maximum_score) * 100.0
            norm = max(0.0, min(100.0, norm))
            contrib = norm * weight
            section_contributions[name] = contrib

            # Build breakdown info
            matched_items: tuple[str, ...] = ()
            missing_items: tuple[str, ...] = ()
            classification_counts: dict[str, int] = {}
            if section.breakdown:
                matched_items = section.breakdown.matched_items
                missing_items = section.breakdown.missing_items
                classification_counts = section.breakdown.classification_counts

            # Timing split metrics
            f_start = time.perf_counter()
            formula = ExplainabilityFormatter.format_section_formula(
                raw_score=section.raw_score,
                maximum_score=section.maximum_score,
                weight_used=weight,
                contribution=contrib,
            )
            formula_gen_time += (time.perf_counter() - f_start) * 1000.0

            fmt_start = time.perf_counter()
            summary = ExplainabilityFormatter.format_section_summary(
                section_name=name,
                raw_score=section.raw_score,
                maximum_score=section.maximum_score,
                normalized_score=norm,
                weight_used=weight,
                matched_count=len(matched_items),
                missing_count=len(missing_items),
            )
            formatting_time += (time.perf_counter() - fmt_start) * 1000.0

            # Construct immutable SectionExplanation DTO
            section_explanations[name] = SectionExplanation(
                section_name=name,
                raw_score=section.raw_score,
                maximum_score=section.maximum_score,
                normalized_score=norm,
                weight_used=weight,
                matched_items=matched_items,
                missing_items=missing_items,
                classification_counts=classification_counts,
                formula=formula,
                summary=summary,
            )

        # Step 3: Explain Overall score (if present)
        overall_explanation: OverallExplanation | None = None
        if score_result.overall_score is not None:
            f_start = time.perf_counter()
            overall_formula = ExplainabilityFormatter.format_overall_formula(
                overall_score=score_result.overall_score,
                contributions=section_contributions,
            )
            formula_gen_time += (time.perf_counter() - f_start) * 1000.0

            fmt_start = time.perf_counter()
            overall_summary = ExplainabilityFormatter.format_overall_summary(
                overall_score=score_result.overall_score
            )
            formatting_time += (time.perf_counter() - fmt_start) * 1000.0

            overall_explanation = OverallExplanation(
                overall_score=score_result.overall_score,
                formula=overall_formula,
                section_contributions=section_contributions,
                weight_configuration_version=self._weight_config.version,
                summary=overall_summary,
            )

        execution_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 4: Build stats and metadata
        stats = ExplainabilityStatisticsBuilder.build(
            execution_time_ms=execution_time_ms,
            sections_processed=sections_processed,
            formula_generation_time_ms=formula_gen_time,
            formatting_time_ms=formatting_time,
            success=True,
        )

        metadata = ExplainabilityMetadataBuilder.build(
            explainability_version=self.EXPLAINER_VERSION,
            pipeline_version=score_result.metadata.pipeline_version,
            framework_version="1.0.0",
        )

        # Step 5: Wrap and return
        return ExplainabilityResult(
            score_result=score_result,
            overall_explanation=overall_explanation,
            section_explanations=section_explanations,
            statistics=stats,
            metadata=metadata,
        )

    def _validate_input(self, score_result: ScoreResult) -> None:
        """Verify ScoreResult validity before explaining."""
        if score_result is None:
            raise ExplainabilityValidationError("ScoreResult cannot be None.")

        # Require all five sections
        sections = [
            ("skill_score", "SKILL"),
            ("experience_score", "EXPERIENCE"),
            ("education_score", "EDUCATION"),
            ("project_score", "PROJECT"),
            ("certification_score", "CERTIFICATION"),
        ]
        for attr, name in sections:
            sec = getattr(score_result, attr, None)
            if sec is None:
                raise ExplainabilityValidationError(
                    f"Validation failed: missing required section '{name}' in ScoreResult."
                )
            if sec.raw_score is None:
                raise ExplainabilityValidationError(
                    f"Validation failed: section '{name}' has a None raw_score."
                )
            if sec.maximum_score is None or sec.maximum_score <= 0:
                raise ExplainabilityValidationError(
                    f"Validation failed: section '{name}' has an invalid maximum_score ({sec.maximum_score!r})."
                )
