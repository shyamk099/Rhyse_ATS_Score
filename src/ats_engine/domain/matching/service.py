"""Service coordinating ATS Matching Engine processes.

Purpose:
    Expose public API to perform matcher evaluations, orchestrate pipeline execution,
    and build verified MatchCollection results.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Mapping, Sequence

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.exceptions import ContextValidationError, MatchingError
from ats_engine.domain.matching.models import MatchCollection, MatchingContext
from ats_engine.domain.matching.pipeline import MatchingPipeline
from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.rules import MatchingRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class MatchingService:
    """Public service orchestrating comparison runs on CanonicalFeatureCollections."""

    def __init__(
        self,
        registry: FeatureMatcherRegistry | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize service with registries and pipelines."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self.registry = registry or FeatureMatcherRegistry()
        self._pipeline = MatchingPipeline(self.registry, self._logger)

    def match(
        self,
        resume_features: CanonicalFeatureCollection,
        job_features: CanonicalFeatureCollection,
        enabled_matchers: Sequence[str],
        rules: Mapping[str, Any] | None = None,
    ) -> MatchCollection:
        """Execute active matchers on resume and job description feature collections.

        Args:
            resume_features: The consolidated Resume FeatureCollection.
            job_features: The consolidated Job Description FeatureCollection.
            enabled_matchers: Sequences of active matcher identifier keys.
            rules: Configuration heuristics overrides.

        Returns:
            The compiled MatchCollection containing comparison DTOs.

        Raises:
            ContextValidationError: If input parameters or collections are missing or invalid.
            MatchingError: For all pipeline execution failures.
        """
        self._logger.info("matching_service_match_called")

        # 1. Input parameter validations
        if resume_features is None:
            raise ContextValidationError("Resume feature collection cannot be None.")
        if job_features is None:
            raise ContextValidationError("Job description feature collection cannot be None.")

        # 2. Resolve rules configuration payload
        rules_payload = dict(rules) if rules else {}
        matching_rules = MatchingRules(
            enabled_matchers=enabled_matchers,
            execution_order=enabled_matchers,
            enable_logging=rules_payload.get("enable_logging", True),
            timeout_seconds=rules_payload.get("timeout_seconds", 30.0),
            rules_version=rules_payload.get("rules_version", "matching_rules_v1.0"),
        )

        # 3. Compile context variables
        corr_id = rules_payload.get("correlation_id") or f"corr-match-{uuid.uuid4().hex[:8]}"

        context = MatchingContext(
            resume_features=resume_features,
            job_features=job_features,
            rule_payload=rules_payload,
            correlation_id=corr_id,
            execution_metadata={
                "rules_version": matching_rules.rules_version,
            },
        )

        # 4. Invoke pipeline execution
        try:
            return self._pipeline.execute(
                context=context,
                enabled_matchers=enabled_matchers,
                rules=matching_rules,
            )
        except Exception as exc:
            self._logger.exception(
                "matching_service_execution_failed",
                extra={"error": str(exc)},
            )
            # Re-raise matching exceptions
            if isinstance(exc, MatchingError):
                raise
            raise MatchingError(f"Failed to execute matching pipeline: {exc}") from exc

