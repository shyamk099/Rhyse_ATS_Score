"""Unit tests for Project Matching.

Purpose:
    Verify ProjectMatcher matching logic, candidate builders, normalizers,
    validators, stats calculations, deterministic sorting, and pipeline integration.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.feature_engineering.models import (
    CanonicalFeatureCollection,
    Feature,
    FeatureCategory,
    FeatureCollection,
    FeatureEngineeringStatistics,
    FeatureExtractionContext,
    FeatureMetadata,
    FeatureProvenance,
    FeatureStatistics,
    ValidationSummary,
)
from ats_engine.domain.matching.models import MatchingContext
from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.service import MatchingService
from ats_engine.domain.matching.project.matcher import ProjectMatcher


class ProjectMatchingTests(unittest.TestCase):
    """Test suite validating ProjectMatcher candidate pipeline and constraints."""

    def setUp(self) -> None:
        """Set up registry and service context."""
        self._registry = FeatureMatcherRegistry()
        self._registry.register("project", ProjectMatcher)
        self._service = MatchingService(self._registry)

    def _create_project_feature(
        self,
        fid: str,
        name: str,
        source_id: str | None,
        org: str | None = None,
        role: str | None = None,
        category: FeatureCategory = FeatureCategory.PROJECT,
    ) -> Feature:
        """Helper to create Feature mock instances."""
        return Feature(
            feature_id=fid,
            name=name,
            category=category,
            value={
                "project_name": name,
                "organization": org,
                "role": role,
            },
            provenance=FeatureProvenance(
                source_entity_id=source_id,
                source_entity_type=category.value,
            ),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="ProjectFeatureExtractor",
                version="1.0",
            ),
        )

    def _create_canonical_collection(self, features: list[Feature]) -> CanonicalFeatureCollection:
        """Helper to compile CanonicalFeatureCollection DTOs."""
        col = FeatureCollection(
            features=tuple(features),
            statistics=FeatureEngineeringStatistics(),
            context=FeatureExtractionContext(correlation_id="test"),
        )
        return CanonicalFeatureCollection(
            skills=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            experience=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            education=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            projects=col,
            certifications=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            statistics=FeatureStatistics(total_feature_count=len(features)),
            validation_summary=ValidationSummary(
                status="VALID",
                validation_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
            ),
        )

    def test_canonical_id_match(self) -> None:
        """ProjectMatcher matches features with identical canonical IDs."""
        f_res = self._create_project_feature("FEAT-PRJ-01", "Project Alpha", "PRJ-01")
        f_job = self._create_project_feature("FEAT-PRJ-01", "Project Alpha V2", "PRJ-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["project"])

        self.assertEqual(1, len(res.results))
        self.assertEqual("FEAT-PRJ-01", res.results[0].resume_feature_id)

    def test_structural_matching_precedence(self) -> None:
        """ProjectMatcher performs matching based on comparison modes and fields."""
        f_res = self._create_project_feature("FEAT-PRJ-RAW-1", "Alpha", None, org="Google", role="SWE")
        f_job = self._create_project_feature("FEAT-PRJ-RAW-2", "Alpha", None, org="Google", role="SWE")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        rules = {
            "project_matching_rules": {
                "comparison_mode": "ALL",
            }
        }
        res = self._service.match(resume, job, ["project"], rules=rules)
        self.assertEqual(1, len(res.results))
