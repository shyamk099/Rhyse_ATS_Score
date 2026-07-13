"""Service engine for Canonical Feature consolidation.

Purpose:
    Provide unified public API to build and validate the CanonicalFeatureCollection.
"""

from __future__ import annotations

import logging

from ats_engine.domain.feature_engineering.exceptions import CanonicalCollectionBuildError
from ats_engine.domain.feature_engineering.models import (
    CanonicalFeatureCollection,
    FeatureCollection,
)
from ats_engine.domain.feature_engineering.canonical.pipeline import CanonicalFeatureCollectionPipeline
from ats_engine.domain.feature_engineering.canonical.rules import CanonicalFeatureValidationRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CanonicalFeatureCollectionService:
    """Service providing consolidation and validation APIs for ATS Downstream modules."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with logs and pipeline dependencies."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._pipeline = CanonicalFeatureCollectionPipeline(self._logger)

    def build(
        self,
        skill_features: FeatureCollection,
        experience_features: FeatureCollection,
        education_features: FeatureCollection,
        project_features: FeatureCollection,
        certification_features: FeatureCollection,
        rules: CanonicalFeatureValidationRules | None = None,
    ) -> CanonicalFeatureCollection:
        """Consolidate domain features into CanonicalFeatureCollection.

        Args:
            skill_features: Skill FeatureCollection.
            experience_features: Experience FeatureCollection.
            education_features: Education FeatureCollection.
            project_features: Project FeatureCollection.
            certification_features: Certification FeatureCollection.
            rules: Configured CanonicalFeatureValidationRules or None.

        Returns:
            The consolidated and verified CanonicalFeatureCollection DTO.

        Raises:
            CanonicalCollectionBuildError: If pipeline consolidation crashes.
        """
        self._logger.info("canonical_feature_collection_service_build_called")

        active_rules = rules or CanonicalFeatureValidationRules()

        try:
            return self._pipeline.execute(
                skills=skill_features,
                experience=experience_features,
                education=education_features,
                projects=project_features,
                certifications=certification_features,
                rules=active_rules,
            )
        except Exception as exc:
            self._logger.exception(
                "canonical_feature_collection_build_failed",
                extra={"error": str(exc)},
            )
            # Re-raise exceptions properly
            if isinstance(exc, ValueError) or "validation failed" in str(exc).lower():
                raise
            raise CanonicalCollectionBuildError(
                f"Failed to build canonical feature collection: {exc}"
            ) from exc
