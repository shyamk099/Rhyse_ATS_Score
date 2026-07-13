"""Unit and Integration tests for Canonical Feature Validation and Collection.

Purpose:
    Verify CanonicalFeatureCollection aggregation, read-only FeatureValidator,
    DuplicateFeatureResolver policies, CrossFeatureValidator consistency checks,
    FeatureStatisticsBuilder, ValidationSummaryBuilder, deterministic ordering,
    and concurrent thread safety.
"""

from __future__ import annotations

import threading
import unittest
from typing import Mapping

from ats_engine.domain.feature_engineering.exceptions import FeatureValidationError
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureCollection,
    FeatureEngineeringStatistics,
    FeatureExtractionContext,
    FeatureLocation,
    FeatureMetadata,
    FeatureProvenance,
)
from ats_engine.domain.feature_engineering.canonical.rules import CanonicalFeatureValidationRules
from ats_engine.domain.feature_engineering.canonical.service import CanonicalFeatureCollectionService
from ats_engine.domain.feature_engineering.canonical.duplicate_resolver import DuplicateFeatureResolver


class CanonicalFeatureCollectionTests(unittest.TestCase):
    """Test suite verifying Canonical Feature validation rules, deduplication, and collection."""

    def setUp(self) -> None:
        """Initialize pipeline service wrapper."""
        self._service = CanonicalFeatureCollectionService()

    def _create_feature(
        self,
        fid: str,
        name: str,
        category: FeatureCategory,
        confidence: float = 0.9,
        source_type: str | None = None,
    ) -> Feature:
        """Helper constructing Feature DTO instances."""
        return Feature(
            feature_id=fid,
            name=name,
            category=category,
            value={},
            confidence=confidence,
            locations=(),
            provenance=FeatureProvenance(
                source_entity_id="ENT-01",
                source_entity_type=source_type or category.value,
                source_section="MOCK",
            ),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="MockExtractor",
                version="1.0",
            ),
        )

    def _create_collection(self, features: list[Feature]) -> FeatureCollection:
        """Helper constructing FeatureCollection wrappers."""
        return FeatureCollection(
            features=tuple(features),
            statistics=FeatureEngineeringStatistics(),
            context=FeatureExtractionContext(correlation_id="test_corr"),
        )

    def test_aggregates_valid_feature_collections(self) -> None:
        """Service compiles individual FeatureCollections into CanonicalFeatureCollection."""
        f_skill = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        f_exp = self._create_feature("FEAT-EXP-01", "Developer", FeatureCategory.EXPERIENCE)
        f_edu = self._create_feature("FEAT-EDU-01", "BS CS", FeatureCategory.EDUCATION)
        f_proj = self._create_feature("FEAT-PROJ-01", "ATS Engine", FeatureCategory.PROJECT)
        f_cert = self._create_feature("FEAT-CERT-01", "AWS PCA", FeatureCategory.CERTIFICATION)

        col = self._service.build(
            skill_features=self._create_collection([f_skill]),
            experience_features=self._create_collection([f_exp]),
            education_features=self._create_collection([f_edu]),
            project_features=self._create_collection([f_proj]),
            certification_features=self._create_collection([f_cert]),
        )

        self.assertEqual(1, len(col.skills.features))
        self.assertEqual(1, len(col.experience.features))
        self.assertEqual("VALID", col.validation_summary.status)
        self.assertEqual(5, col.statistics.total_feature_count)
        self.assertEqual(1, col.statistics.category_counts["SKILL"])

    def test_deterministic_ordering_applied(self) -> None:
        """Category features are sorted deterministically by feature_id (Refinement 5)."""
        f3 = self._create_feature("FEAT-SKILL-03", "C++", FeatureCategory.SKILL)
        f1 = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        f2 = self._create_feature("FEAT-SKILL-02", "Go", FeatureCategory.SKILL)

        col = self._service.build(
            skill_features=self._create_collection([f3, f1, f2]),
            experience_features=self._create_collection([]),
            education_features=self._create_collection([]),
            project_features=self._create_collection([]),
            certification_features=self._create_collection([]),
        )

        self.assertEqual("FEAT-SKILL-01", col.skills.features[0].feature_id)
        self.assertEqual("FEAT-SKILL-02", col.skills.features[1].feature_id)
        self.assertEqual("FEAT-SKILL-03", col.skills.features[2].feature_id)

    def test_duplicate_resolution_policies(self) -> None:
        """Deduplication supports KEEP_FIRST, KEEP_LAST, and KEEP_HIGHEST_CONFIDENCE policies."""
        f1 = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL, confidence=0.8)
        f2 = self._create_feature("FEAT-SKILL-01", "Python V2", FeatureCategory.SKILL, confidence=0.95)

        resolver = DuplicateFeatureResolver()

        # KEEP_FIRST
        res_first, count = resolver.resolve([f1, f2], "KEEP_FIRST")
        self.assertEqual(1, len(res_first))
        self.assertEqual(0.8, res_first[0].confidence)
        self.assertEqual(1, count)

        # KEEP_LAST
        res_last, count = resolver.resolve([f1, f2], "KEEP_LAST")
        self.assertEqual(1, len(res_last))
        self.assertEqual(0.95, res_last[0].confidence)

        # KEEP_HIGHEST_CONFIDENCE
        res_high, count = resolver.resolve([f1, f2], "KEEP_HIGHEST_CONFIDENCE")
        self.assertEqual(1, len(res_high))
        self.assertEqual(0.95, res_high[0].confidence)

        # KEEP_ALL
        res_all, count = resolver.resolve([f1, f2], "KEEP_ALL")
        self.assertEqual(2, len(res_all))
        self.assertEqual(0, count)

    def test_validation_strictness_raises_exception(self) -> None:
        """Service raises FeatureValidationError if features are invalid (low confidence, etc.)."""
        # Duplicate feature IDs under KEEP_ALL resolution policy triggers cross-validation INVALID status
        f1 = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        f2 = self._create_feature("FEAT-SKILL-01", "Python Duplicate", FeatureCategory.SKILL)
        
        rules = CanonicalFeatureValidationRules(duplicate_policy="KEEP_ALL")
        with self.assertRaises(FeatureValidationError):
            self._service.build(
                skill_features=self._create_collection([f1, f2]),
                experience_features=self._create_collection([]),
                education_features=self._create_collection([]),
                project_features=self._create_collection([]),
                certification_features=self._create_collection([]),
                rules=rules,
            )

    def test_cross_validation_mismatched_provenance_warning(self) -> None:
        """CrossFeatureValidator flags warning if feature category and provenance source_entity_type mismatch."""
        f1 = self._create_feature(
            fid="FEAT-SKILL-01",
            name="Python Mismatch",
            category=FeatureCategory.SKILL,
            source_type="EXPERIENCE",  # mismatched
        )

        col = self._service.build(
            skill_features=self._create_collection([f1]),
            experience_features=self._create_collection([]),
            education_features=self._create_collection([]),
            project_features=self._create_collection([]),
            certification_features=self._create_collection([]),
        )

        self.assertEqual("WARNING", col.validation_summary.status)
        self.assertEqual(1, len(col.validation_summary.warnings))
        self.assertEqual("mismatched_provenance_type", col.validation_summary.warnings[0].warning_type)

    def test_empty_collections_resilient(self) -> None:
        """Service is resilient to empty lists and returns a valid collection with 0 feature stats."""
        col = self._service.build(
            skill_features=self._create_collection([]),
            experience_features=self._create_collection([]),
            education_features=self._create_collection([]),
            project_features=self._create_collection([]),
            certification_features=self._create_collection([]),
        )
        self.assertEqual(0, col.statistics.total_feature_count)
        self.assertEqual("VALID", col.validation_summary.status)

    def test_thread_safety_under_concurrent_resolutions(self) -> None:
        """Service executes concurrently without shared mutable state failures."""
        f_skill = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        f_exp = self._create_feature("FEAT-EXP-01", "Developer", FeatureCategory.EXPERIENCE)

        errors: list[Exception] = []

        def run_compilation() -> None:
            try:
                col = self._service.build(
                    skill_features=self._create_collection([f_skill]),
                    experience_features=self._create_collection([f_exp]),
                    education_features=self._create_collection([]),
                    project_features=self._create_collection([]),
                    certification_features=self._create_collection([]),
                )
                self.assertEqual(2, col.statistics.total_feature_count)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_compilation) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Concurrent collection build failed: {errors}")
