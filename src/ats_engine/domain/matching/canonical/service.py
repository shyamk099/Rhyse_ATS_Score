"""CanonicalMatchCollectionService class.

Purpose:
    Provide the primary service entrypoint coordinate aggregation and validation of
    individual MatchCollections into a consolidated CanonicalMatchCollection DTO.
"""

from __future__ import annotations

import logging

from ats_engine.domain.matching.models import MatchCollection, CanonicalMatchCollection
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules
from ats_engine.domain.matching.canonical.pipeline import CanonicalMatchCollectionPipeline
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CanonicalMatchCollectionService:
    """Service providing consolidation and validation API for Book 05 match results."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with its pipeline dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._pipeline = CanonicalMatchCollectionPipeline(self._logger)

    def build(
        self,
        skill_matches: MatchCollection,
        experience_matches: MatchCollection,
        education_matches: MatchCollection,
        project_matches: MatchCollection,
        certification_matches: MatchCollection,
        rules: CanonicalMatchingRules | None = None,
    ) -> CanonicalMatchCollection:
        """Consolidate individual matcher collections into a CanonicalMatchCollection.

        Args:
            skill_matches: Skill matcher output collection.
            experience_matches: Experience matcher output collection.
            education_matches: Education matcher output collection.
            project_matches: Project matcher output collection.
            certification_matches: Certification matcher output collection.
            rules: Configuration rules payload. Defaults to default CanonicalMatchingRules.

        Returns:
            The consolidated, immutable CanonicalMatchCollection.
        """
        active_rules = rules or CanonicalMatchingRules()
        
        self._logger.info(
            "canonical_match_collection_build_started",
            extra={
                "rules_version": active_rules.rules_version,
                "validation_mode": active_rules.validation_mode,
            },
        )

        collection = self._pipeline.execute(
            skill_matches=skill_matches,
            experience_matches=experience_matches,
            education_matches=education_matches,
            project_matches=project_matches,
            certification_matches=certification_matches,
            rules=active_rules,
        )

        self._logger.info(
            "canonical_match_collection_build_completed",
            extra={
                "total_matches": len(collection.results),
                "total_errors": collection.validation_summary.total_errors,
                "total_warnings": collection.validation_summary.total_warnings,
            },
        )

        return collection
