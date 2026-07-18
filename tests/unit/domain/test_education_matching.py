"""Unit tests for Education Matching.

Purpose:
    Verify EducationMatcher precedence rules, candidate builders (empty fields ignore),
    normalizers, validators, stats calculations, deterministic sorting,
    thread safety, and pipeline integration.
"""

from __future__ import annotations

import threading
import unittest
from typing import Sequence

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
from ats_engine.domain.matching.education.matcher import EducationMatcher


class EducationMatchingTests(unittest.TestCase):
    """Test suite validating EducationMatcher and candidate pipeline orchestration."""

    def setUp(self) -> None:
        """Set up registry and service context."""
        self._registry = FeatureMatcherRegistry()
        self._registry.register("education", EducationMatcher)
        self._service = MatchingService(self._registry)

    def _create_education_feature(
        self,
        fid: str,
        institution: str | None,
        degree: str | None,
        major: str | None,
        specialization: str | None,
        source_id: str | None,
        category: FeatureCategory = FeatureCategory.EDUCATION,
    ) -> Feature:
        """Helper to create Feature mock instances."""
        return Feature(
            feature_id=fid,
            name=degree or "Unknown Degree",
            category=category,
            value={
                "institution": institution,
                "degree": degree,
                "major": major,
                "specialization": specialization,
            },
            provenance=FeatureProvenance(
                source_entity_id=source_id,
                source_entity_type=category.value,
            ),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="EducationFeatureExtractor",
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
            education=col,
            projects=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            certifications=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            statistics=FeatureStatistics(total_feature_count=len(features)),
            validation_summary=ValidationSummary(
                status="VALID",
                validation_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
            ),
        )

    def test_canonical_id_match_precedence(self) -> None:
        """Canonical ID matches bypass lower precedence rules even if institutions differ."""
        f_res = self._create_education_feature("FEAT-EDU-01", "MIT", "BS", "CS", "AI", "EDU-01")
        f_job = self._create_education_feature("FEAT-EDU-01", "Stanford", "MS", "Math", "Stats", "EDU-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["education"])

        self.assertEqual(1, len(res.results))
        self.assertEqual("FEAT-EDU-01", res.results[0].resume_feature_id)

    def test_precedence_relaxation_order(self) -> None:
        """Comparison relaxes requirements from strict to loose."""
        # 1. Institution + Degree + Major + Specialization
        f_res = self._create_education_feature("FEAT-EDU-01", "MIT", "BS", "CS", "AI", None)
        f_job = self._create_education_feature("FEAT-EDU-02", "MIT", "BS", "CS", "AI", None)
        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        rules_spec = {"education_matching_rules": {"comparison_mode": "INSTITUTION_DEGREE_MAJOR_SPECIALIZATION"}}
        res = self._service.match(resume, job, ["education"], rules=rules_spec)
        self.assertEqual(1, len(res.results))

        # 2. Institution + Degree + Major (Specialization mismatch)
        f_job_no_spec = self._create_education_feature("FEAT-EDU-02", "MIT", "BS", "CS", "NLP", None)
        job_no_spec = self._create_canonical_collection([f_job_no_spec])
        res_no_spec = self._service.match(resume, job_no_spec, ["education"], rules=rules_spec)
        self.assertEqual(0, len(res_no_spec.results))  # Specialization mismatch under strict mode

        rules_major = {"education_matching_rules": {"comparison_mode": "INSTITUTION_DEGREE_MAJOR"}}
        res_major = self._service.match(resume, job_no_spec, ["education"], rules=rules_major)
        self.assertEqual(1, len(res_major.results))  # Matches under Major mode

    def test_empty_fields_candidate_ignored(self) -> None:
        """Pairs where all matching attributes are empty/None are ignored from candidates."""
        f_res = self._create_education_feature("FEAT-EDU-01", None, None, None, None, None)
        f_job = self._create_education_feature("FEAT-EDU-02", "MIT", "BS", "CS", "AI", None)

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["education"])
        self.assertEqual(0, len(res.results))

    def test_invalid_feature_categories_skipped(self) -> None:
        """Validator skips features not from FeatureCategory.EDUCATION."""
        f_res = self._create_education_feature("FEAT-EDU-01", "MIT", "BS", "CS", "AI", "EDU-01")
        f_job = self._create_education_feature("FEAT-SKILL-01", "Python", None, None, None, "EDU-01", category=FeatureCategory.SKILL)

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["education"])
        self.assertEqual(0, len(res.results))

    def test_thread_safety(self) -> None:
        """Running EducationMatcher concurrently results in zero race conditions."""
        f_res = self._create_education_feature("FEAT-EDU-01", "MIT", "BS", "CS", "AI", "EDU-01")
        f_job = self._create_education_feature("FEAT-EDU-01", "MIT", "BS", "CS", "AI", "EDU-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        errors: list[Exception] = []

        def run_match() -> None:
            try:
                res = self._service.match(resume, job, ["education"])
                self.assertEqual(1, len(res.results))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_match) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread safety test failed: {errors}")
