"""Pipeline executing consolidation, validation, and statistics aggregation.

Purpose:
    Execute sequential processing steps to transform raw match collections into
    a CanonicalMatchCollection.
"""

from __future__ import annotations

import logging
import time
from typing import Sequence

from ats_engine.domain.matching.models import MatchResult, CanonicalMatchCollection, MatchCollection
from ats_engine.domain.matching.exceptions import (
    MatchValidationError,
    CrossMatchValidationError,
    CanonicalMatchCollectionBuildError,
)
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules
from ats_engine.domain.matching.canonical.validator import MatchValidator
from ats_engine.domain.matching.canonical.duplicate_resolver import DuplicateMatchResolver
from ats_engine.domain.matching.canonical.cross_validator import CrossMatchValidator
from ats_engine.domain.matching.canonical.stats_builder import MatchStatisticsBuilder
from ats_engine.domain.matching.canonical.validation_summary_builder import ValidationSummaryBuilder
from ats_engine.domain.matching.canonical.builder import CanonicalMatchCollectionBuilder
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CanonicalMatchCollectionPipeline:
    """Pipeline orchestrator running validation, deduplication, and consolidation."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize pipeline with optional custom logger."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def execute(
        self,
        skill_matches: MatchCollection,
        experience_matches: MatchCollection,
        education_matches: MatchCollection,
        project_matches: MatchCollection,
        certification_matches: MatchCollection,
        rules: CanonicalMatchingRules,
    ) -> CanonicalMatchCollection:
        """Run consolidation and validation pipeline steps.

        Args:
            skill_matches: Skill matcher output collection.
            experience_matches: Experience matcher output collection.
            education_matches: Education matcher output collection.
            project_matches: Project matcher output collection.
            certification_matches: Certification matcher output collection.
            rules: Configured pipeline rules.

        Returns:
            The consolidated CanonicalMatchCollection.

        Raises:
            MatchValidationError: If strict validation fails on matcher results.
            CrossMatchValidationError: If strict cross-validation invariants are violated.
            CanonicalMatchCollectionBuildError: For internal pipeline execution faults.
        """
        start_time = time.perf_counter()

        try:
            # 1. Combine inputs
            all_collections = [
                skill_matches,
                experience_matches,
                education_matches,
                project_matches,
                certification_matches,
            ]
            
            combined_results: list[MatchResult] = []
            total_resume_features = 0
            total_job_features = 0

            for collection in all_collections:
                if collection.results:
                    combined_results.extend(collection.results)
                # Count total resume and job features if context/stats are present
                if collection.statistics:
                    total_resume_features += getattr(collection.statistics, "total_resume_features", 0)
                    total_job_features += getattr(collection.statistics, "total_job_features", 0)

            # 2. Structural Validation
            validation_errors = MatchValidator.validate(combined_results, rules)
            if validation_errors and rules.validation_mode == "STRICT":
                self._logger.error("strict_match_validation_failed", extra={"errors": validation_errors})
                raise MatchValidationError(f"Match validation failed with {len(validation_errors)} errors.")

            # 3. Deduplication
            resolved_results, duplicate_count = DuplicateMatchResolver.resolve(combined_results, rules)

            # 4. Cross-collection Validation
            cross_errors, warnings = CrossMatchValidator.validate(resolved_results, rules)
            if cross_errors and rules.validation_mode == "STRICT":
                self._logger.error("strict_cross_validation_failed", extra={"errors": cross_errors})
                raise CrossMatchValidationError(f"Cross-match validation failed with {len(cross_errors)} errors.")

            # Combine structural validation errors and cross validation errors
            all_errors = validation_errors + cross_errors

            # 5. Compile validation summary
            validation_summary = ValidationSummaryBuilder.build(all_errors, warnings)

            # 6. Build execution statistics
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            statistics = MatchStatisticsBuilder.build(
                results=resolved_results,
                total_resume_features=total_resume_features,
                total_job_features=total_job_features,
                duplicate_count=duplicate_count,
                validation_error_count=len(all_errors),
                warning_count=len(warnings),
                execution_duration_ms=duration_ms,
            )

            # 7. Package and return the final DTO
            return CanonicalMatchCollectionBuilder.build(
                results=resolved_results,
                statistics=statistics,
                validation_summary=validation_summary,
                rules=rules,
            )

        except (MatchValidationError, CrossMatchValidationError):
            raise
        except Exception as e:
            self._logger.exception("canonical_pipeline_execution_fault")
            raise CanonicalMatchCollectionBuildError(f"Canonical pipeline execution failed: {str(e)}") from e
