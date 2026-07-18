"""Unit tests for Experience Matching.

Purpose:
    Verify ExperienceMatcher exact matching logic, candidate builders, normalizers,
    validators, stats calculations, deterministic sorting, thread safety,
    and pipeline integration.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any, Mapping, Sequence

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
from ats_engine.domain.matching.experience.matcher import ExperienceMatcher


class ExperienceMatchingTests(unittest.TestCase):
    """Test suite validating ExperienceMatcher and candidate pipeline consolidation."""

    def setUp(self) -> None:
        """Set up registry and service context."""
        self._registry = FeatureMatcherRegistry()
        self._registry.register("experience", ExperienceMatcher)
        self._service = MatchingService(self._registry)

    def _create_experience_feature(
        self,
        fid: str,
        company: str,
        title: str,
        source_id: str | None,
        category: FeatureCategory = FeatureCategory.EXPERIENCE,
    ) -> Feature:
        """Helper to create Feature mock instances."""
        return Feature(
            feature_id=fid,
            name=title,
            category=category,
            value={
                "company": company,
                "job_title": title,
                "employment_type": "Full-time",
            },
            provenance=FeatureProvenance(
                source_entity_id=source_id,
                source_entity_type=category.value,
            ),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="ExperienceFeatureExtractor",
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
            experience=col,
            education=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            projects=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            certifications=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            statistics=FeatureStatistics(total_feature_count=len(features)),
            validation_summary=ValidationSummary(
                status="VALID",
                validation_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
            ),
        )

    def test_exact_canonical_id_match(self) -> None:
        """ExperienceMatcher matches features with identical canonical IDs."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "Google", "SWE", "EXP-01")
        f_job = self._create_experience_feature("FEAT-EXP-01", "Alphabet", "Engineer", "EXP-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["experience"])

        self.assertEqual(1, len(res.results))
        self.assertEqual("FEAT-EXP-01", res.results[0].resume_feature_id)
        self.assertEqual("FEAT-EXP-01", res.results[0].job_feature_id)

    def test_no_match_for_mismatched_ids_in_canonical_mode(self) -> None:
        """ExperienceMatcher skips features with different canonical IDs in default CANONICAL mode."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "Google", "SWE", "EXP-01")
        f_job = self._create_experience_feature("FEAT-EXP-02", "Google", "SWE", "EXP-02")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["experience"])
        self.assertEqual(0, len(res.results))

    def test_company_title_equality_match(self) -> None:
        """ExperienceMatcher matches features by company and title under COMPANY_TITLE mode."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "  Google  ", "SWE", None)
        f_job = self._create_experience_feature("FEAT-EXP-02", "Google", "SWE", None)

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        rules = {
            "experience_matching_rules": {
                "comparison_mode": "COMPANY_TITLE",
            }
        }
        res = self._service.match(resume, job, ["experience"], rules=rules)
        self.assertEqual(1, len(res.results))

    def test_invalid_feature_categories_skipped(self) -> None:
        """Validator/Builder skips features that are not from FeatureCategory.EXPERIENCE."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "Google", "SWE", "EXP-01")
        f_job = self._create_experience_feature("FEAT-SKILL-01", "Python", "SkillTitle", "EXP-01", category=FeatureCategory.SKILL)

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["experience"])
        self.assertEqual(0, len(res.results))

    def test_read_only_and_trim_normalization(self) -> None:
        """Trims whitespace collapse without mutating the original Feature attributes."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "  Google  Inc  ", "SWE", "EXP-01")
        f_job = self._create_experience_feature("FEAT-EXP-01", "Google Inc", "SWE", "EXP-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["experience"])
        self.assertEqual(1, len(res.results))

        # Original name and value dict remain unmutated (Rule 5)
        self.assertEqual("  Google  Inc  ", f_res.value.get("company"))

    def test_thread_safety(self) -> None:
        """Running ExperienceMatcher concurrently results in zero race conditions."""
        f_res = self._create_experience_feature("FEAT-EXP-01", "Google", "SWE", "EXP-01")
        f_job = self._create_experience_feature("FEAT-EXP-01", "Google", "SWE", "EXP-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        errors: list[Exception] = []

        def run_match() -> None:
            try:
                res = self._service.match(resume, job, ["experience"])
                self.assertEqual(1, len(res.results))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_match) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread safety test failed: {errors}")
