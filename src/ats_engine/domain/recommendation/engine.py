"""RecommendationEngine implementation.

Purpose:
    Coordinate the recommendation pipeline — validate inputs, execute registered
    providers in deterministic priority order, and return an immutable
    RecommendationResult.

    This milestone produces a framework-only engine: with no providers registered,
    the engine returns an empty recommendations tuple.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult
from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.validator import RecommendationValidator
from ats_engine.domain.recommendation.statistics_builder import RecommendationStatisticsBuilder
from ats_engine.domain.recommendation.metadata_builder import RecommendationMetadataBuilder
from ats_engine.domain.recommendation.exceptions import (
    RecommendationError,
    RecommendationProviderError,
)
from ats_engine.infrastructure.logging.factory import LoggerFactory
from ats_engine.domain.recommendation.post_processors.base import BasePostProcessor


class RecommendationEngine:
    """Deterministic recommendation engine coordinating provider execution.

    The engine:
        1. Validates inputs wrapping them in RecommendationContext.
        2. Validates registry (unique priorities, no duplicates).
        3. Iterates providers in deterministic priority order.
        4. Calls provider.validate() then provider.generate() with context.
        5. Merges all Recommendation tuples into a single result.
        6. Wraps everything in an immutable RecommendationResult.

    The engine NEVER:
        - Generates recommendations itself.
        - Uses AI, LLMs, or embeddings.
        - Modifies upstream DTOs.
    """

    ENGINE_VERSION: str = "1.0.0"

    def __init__(
        self,
        registry: RecommendationRegistry | None = None,
        logger: logging.Logger | None = None,
        post_processors: list[BasePostProcessor] | None = None,
    ) -> None:
        """Initialize the engine.

        Args:
            registry: The RecommendationRegistry containing providers.
                      Defaults to an empty registry if None.
            logger: Optional logger.
            post_processors: Optional list of post processors to apply sequentially.
        """
        self._registry = registry or RecommendationRegistry()
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._post_processors = post_processors or []

    @property
    def registry(self) -> RecommendationRegistry:
        """Return the active RecommendationRegistry."""
        return self._registry

    @property
    def post_processors(self) -> list[BasePostProcessor]:
        """Return the active post processors list."""
        return self._post_processors

    def recommend(self, context: RecommendationContext) -> Any:
        """Execute the recommendation pipeline.

        Args:
            context: The RecommendationContext containing match, scoring, and explainability results.

        Returns:
            An immutable RecommendationResult or a prioritized result if PrioritizationEngine post-processor is configured.

        Raises:
            RecommendationValidationError: If inputs fail validation.
            RecommendationProviderError: If any provider fails execution.
            RecommendationError: If an unexpected error occurs.
        """
        start_time = time.perf_counter()

        # Step 1 — Validate inputs
        RecommendationValidator.validate_inputs(context)

        # Step 2 — Validate registry
        RecommendationValidator.validate_registry(self._registry)

        # Step 3 — Execute providers in deterministic order
        all_recommendations: list[Recommendation] = []
        providers_executed: list[str] = []
        providers = self._registry.get_ordered_providers()

        for provider in providers:
            name = provider.provider_name()
            try:
                provider.validate(context)
                results = provider.generate(context)
                all_recommendations.extend(results)
                providers_executed.append(name)
                self._logger.debug(
                    "recommendation_provider_executed",
                    extra={"provider": name, "count": len(results)},
                )
            except RecommendationProviderError:
                self._logger.exception("recommendation_provider_failed", extra={"provider": name})
                raise
            except Exception as exc:
                self._logger.exception("recommendation_provider_unexpected_error", extra={"provider": name})
                raise RecommendationError(
                    f"Provider '{name}' failed unexpectedly: {exc}"
                ) from exc

        execution_time_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 4 — Build statistics and metadata
        stats = RecommendationStatisticsBuilder.build(
            execution_time_ms=execution_time_ms,
            providers_executed=tuple(providers_executed),
            recommendations_generated=len(all_recommendations),
            success=True,
        )

        metadata = RecommendationMetadataBuilder.build(
            recommendation_version=self.ENGINE_VERSION,
            pipeline_version=context.score_result.metadata.pipeline_version,
        )

        # Step 5 — Return immutable result
        res = RecommendationResult(
            context=context,
            recommendations=tuple(all_recommendations),
            statistics=stats,
            metadata=metadata,
        )

        # Step 6 — Run post-processors
        for processor in self._post_processors:
            res = processor.process(res)

        return res

