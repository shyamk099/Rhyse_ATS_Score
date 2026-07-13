"""Pipeline coordinator executing canonical consolidation and validation.

Purpose:
    Sequence validation, deduplication, cross-validation checks, and DTO assembly
    to construct a CanonicalFeatureCollection.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.feature_engineering.exceptions import FeatureValidationError
from ats_engine.domain.feature_engineering.models import (
    CanonicalFeatureCollection,
    Feature,
    FeatureCategory,
    FeatureCollection,
)
from ats_engine.domain.feature_engineering.canonical.builder import CanonicalFeatureCollectionBuilder
from ats_engine.domain.feature_engineering.canonical.cross_validator import CrossFeatureValidator
from ats_engine.domain.feature_engineering.canonical.duplicate_resolver import DuplicateFeatureResolver
from ats_engine.domain.feature_engineering.canonical.rules import CanonicalFeatureValidationRules
from ats_engine.domain.feature_engineering.canonical.stats_builder import FeatureStatisticsBuilder
from ats_engine.domain.feature_engineering.canonical.validation_summary_builder import ValidationSummaryBuilder
from ats_engine.domain.feature_engineering.canonical.validator import FeatureValidator
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CanonicalFeatureCollectionPipeline:
    """Coordinator executing the canonical feature validation and consolidation pipeline."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize pipeline with sub-components."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._validator = FeatureValidator(self._logger)
        self._resolver = DuplicateFeatureResolver()
        self._cross_validator = CrossFeatureValidator(self._logger)

    def execute(
        self,
        skills: FeatureCollection,
        experience: FeatureCollection,
        education: FeatureCollection,
        projects: FeatureCollection,
        certifications: FeatureCollection,
        rules: CanonicalFeatureValidationRules,
    ) -> CanonicalFeatureCollection:
        """Run consolidated validation, deduplication, and compile the final collection DTO.

        Args:
            skills: Skill FeatureCollection.
            experience: Experience FeatureCollection.
            education: Education FeatureCollection.
            projects: Project FeatureCollection.
            certifications: Certification FeatureCollection.
            rules: Active CanonicalFeatureValidationRules config.

        Returns:
            The immutable CanonicalFeatureCollection.

        Raises:
            FeatureValidationError: If validation errors are encountered.
        """
        self._logger.info("canonical_feature_collection_pipeline_started")

        # 1. Gather all features
        all_features: list[Feature] = []
        all_features.extend(skills.features)
        all_features.extend(experience.features)
        all_features.extend(education.features)
        all_features.extend(projects.features)
        all_features.extend(certifications.features)

        # 2. Run Individual Feature Validation
        errors, warnings = self._validator.validate(all_features, rules)

        # 3. Resolve duplicates
        deduped_features, duplicate_count = self._resolver.resolve(
            all_features,
            rules.duplicate_policy,
        )

        # 4. Run Cross-collection consistency checks
        cross_errors, cross_warnings = self._cross_validator.validate(
            deduped_features,
            rules,
        )
        errors.extend(cross_errors)
        warnings.extend(cross_warnings)

        # 5. Build Statistics DTO
        stats = FeatureStatisticsBuilder.build(
            features=deduped_features,
            duplicate_count=duplicate_count,
            error_count=len(errors),
            warning_count=len(warnings),
        )

        # 6. Build Validation Summary DTO
        summary = ValidationSummaryBuilder.build(
            errors=errors,
            warnings=warnings,
            duplicate_count=duplicate_count,
            rules_version=rules.rules_version,
        )

        # Raise validation exception if invalid
        if summary.status == "INVALID":
            self._logger.error(
                "canonical_validation_failed",
                extra={"errors_count": len(errors), "errors": [e.model_dump() for e in errors]},
            )
            raise FeatureValidationError(
                f"Feature validation failed with {len(errors)} errors. Status is INVALID."
            )

        # 7. Group back to individual category containers for the DTO
        skills_resolved: list[Feature] = []
        exp_resolved: list[Feature] = []
        edu_resolved: list[Feature] = []
        proj_resolved: list[Feature] = []
        cert_resolved: list[Feature] = []

        for f in deduped_features:
            cat = f.category
            if cat == FeatureCategory.SKILL:
                skills_resolved.append(f)
            elif cat == FeatureCategory.EXPERIENCE:
                exp_resolved.append(f)
            elif cat == FeatureCategory.EDUCATION:
                edu_resolved.append(f)
            elif cat == FeatureCategory.PROJECT:
                proj_resolved.append(f)
            elif cat == FeatureCategory.CERTIFICATION:
                cert_resolved.append(f)

        skills_col = FeatureCollection(
            features=tuple(skills_resolved),
            statistics=skills.statistics,
            context=skills.context,
        )
        experience_col = FeatureCollection(
            features=tuple(exp_resolved),
            statistics=experience.statistics,
            context=experience.context,
        )
        education_col = FeatureCollection(
            features=tuple(edu_resolved),
            statistics=education.statistics,
            context=education.context,
        )
        projects_col = FeatureCollection(
            features=tuple(proj_resolved),
            statistics=projects.statistics,
            context=projects.context,
        )
        certifications_col = FeatureCollection(
            features=tuple(cert_resolved),
            statistics=certifications.statistics,
            context=certifications.context,
        )

        # 8. Build final collection (Sorting is deterministic inside Builder)
        collection = CanonicalFeatureCollectionBuilder.build(
            skills=skills_col,
            experience=experience_col,
            education=education_col,
            projects=projects_col,
            certifications=certifications_col,
            statistics=stats,
            validation_summary=summary,
        )

        self._logger.info("canonical_feature_collection_pipeline_completed")
        return collection
