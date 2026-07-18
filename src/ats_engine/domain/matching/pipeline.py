"""Matching Pipeline orchestrator.

Purpose:
    Sequence validation, dynamic resolving of matchers from registry, factory instantiation,
    concurrency/execution tracking, and DTO compilation.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.exceptions import PipelineExecutionError, UnknownMatcherError
from ats_engine.domain.matching.factory import FeatureMatcherFactory
from ats_engine.domain.matching.models import (
    MatchCollection,
    MatchingContext,
    MatchingStatistics,
    MatchResult,
)
from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.rules import MatchingRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class MatchingPipeline:
    """Orchestrator running registered FeatureMatchers and aggregating MatchResults."""

    def __init__(
        self,
        registry: FeatureMatcherRegistry,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize pipeline with matcher registry."""
        self._registry = registry
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def _collect_features(self, collection) -> list[Feature]:
        """Flatten canonical collection features into a single sequence."""
        features: list[Feature] = []
        if collection.skills and collection.skills.features:
            features.extend(collection.skills.features)
        if collection.experience and collection.experience.features:
            features.extend(collection.experience.features)
        if collection.education and collection.education.features:
            features.extend(collection.education.features)
        if collection.projects and collection.projects.features:
            features.extend(collection.projects.features)
        if collection.certifications and collection.certifications.features:
            features.extend(collection.certifications.features)
        return features

    def execute(
        self,
        context: MatchingContext,
        enabled_matchers: Sequence[str],
        rules: MatchingRules,
    ) -> MatchCollection:
        """Execute active matchers, compile telemetry, and return MatchCollection.

        Args:
            context: Context containing resume/job collections.
            enabled_matchers: Identifiers of matchers to run.
            rules: MatchingRules rules configuration.

        Returns:
            The immutable MatchCollection.

        Raises:
            PipelineExecutionError: If execution fails or resolves unknown matchers.
        """
        start_time = time.perf_counter()

        self._logger.info(
            "matching_pipeline_execution_started",
            extra={"correlation_id": context.correlation_id},
        )

        resume_feats = self._collect_features(context.resume_features)
        job_feats = self._collect_features(context.job_features)

        results: list[MatchResult] = []
        processed_matchers = 0

        # Execute enabled matchers sequentially
        for matcher_name in enabled_matchers:
            try:
                matcher_cls = self._registry.get(matcher_name)
            except Exception as exc:
                self._logger.error(
                    "matching_pipeline_unresolved_matcher",
                    extra={"matcher_name": matcher_name, "error": str(exc)},
                )
                raise UnknownMatcherError(
                    f"Matcher '{matcher_name}' was not found in the registry."
                ) from exc

            # Instantiate using factory
            matcher_inst = FeatureMatcherFactory.create(matcher_cls)

            try:
                matcher_results = matcher_inst.match(
                    resume_features=resume_feats,
                    job_features=job_feats,
                    context=context,
                )
                results.extend(matcher_results)
                processed_matchers += 1
            except Exception as exc:
                self._logger.exception(
                    "matching_pipeline_matcher_execution_failed",
                    extra={"matcher_name": matcher_name, "error": str(exc)},
                )
                raise PipelineExecutionError(
                    f"Execution of matcher '{matcher_name}' failed: {exc}"
                ) from exc

        # Deterministic sorting (Rule 5)
        # 1. matcher_type
        # 2. resume_feature_id
        # 3. job_feature_id
        sorted_results = sorted(
            results,
            key=lambda r: (r.matcher_type, r.resume_feature_id, r.job_feature_id),
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Compile structural MatchingStatistics
        stats = MatchingStatistics(
            total_resume_features=len(resume_feats),
            total_job_features=len(job_feats),
            processed_features=len(resume_feats) + len(job_feats),
            processed_matchers=processed_matchers,
            match_result_count=len(sorted_results),
            execution_duration_ms=duration_ms,
        )

        self._logger.info(
            "matching_pipeline_execution_completed",
            extra={
                "correlation_id": context.correlation_id,
                "stats": stats.model_dump(),
            },
        )

        return MatchCollection(
            results=tuple(sorted_results),
            statistics=stats,
            context=context,
        )
