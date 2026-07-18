"""Unit tests for Canonical Match Collection & Validation.

Purpose:
    Verify CanonicalMatchCollection pipeline, validation summary building,
    duplicate resolution policies, cross-collection validation, deterministic ordering,
    immutability constraints, empty collections, and stateless execution.
"""

from __future__ import annotations

import threading
import unittest
from typing import Sequence

from pydantic import ValidationError

from ats_engine.domain.feature_engineering.models import FeatureProvenance
from ats_engine.domain.matching.models import (
    MatchResult,
    MatchMetadata,
    MatchLocation,
    MatchCollection,
    MatchingStatistics,
    ValidationErrorDetail,
    ValidationWarningDetail,
    ValidationSummary,
    MatchStatistics,
    CanonicalMatchCollection,
)
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
from ats_engine.domain.matching.canonical.pipeline import CanonicalMatchCollectionPipeline
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService


class CanonicalMatchCollectionTests(unittest.TestCase):
    """Test suite validating CanonicalMatchCollection creation, pipelines, and constraints."""

    def setUp(self) -> None:
        """Initialize service instance."""
        self._service = CanonicalMatchCollectionService()

    def _create_match_result(
        self,
        match_id: str,
        matcher_type: str,
        resume_feat_id: str,
        job_feat_id: str,
        confidence: float = 1.0,
        prov: bool = True,
    ) -> MatchResult:
        """Helper to construct dummy MatchResult DTOs."""
        return MatchResult(
            match_id=match_id,
            matcher_type=matcher_type,
            resume_feature_id=resume_feat_id,
            job_feature_id=job_feat_id,
            metadata=MatchMetadata(
                correlation_id="corr-test",
                matcher_type=matcher_type,
                execution_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
                custom_attributes={"confidence": confidence},
            ),
            provenance=FeatureProvenance(
                source_entity_id="entity-1",
                source_entity_type="test",
            ) if prov else None,
            locations=MatchLocation(
                resume_source_ids=("r1",),
                job_source_ids=("j1",),
            ),
        )

    def _create_match_collection(self, results: Sequence[MatchResult]) -> MatchCollection:
        """Helper to wrap MatchResults into a MatchCollection DTO."""
        return MatchCollection(
            results=tuple(results),
            statistics=MatchingStatistics(
                total_resume_features=10,
                total_job_features=12,
                processed_features=22,
                processed_matchers=1,
                match_result_count=len(results),
            ),
        )

    def test_happy_path_pipeline(self) -> None:
        """Pipeline successfully consolidates and validates well-formed inputs."""
        r1 = self._create_match_result("M1", "SkillMatcher", "R-SK-1", "J-SK-1")
        r2 = self._create_match_result("M2", "ExperienceMatcher", "R-EX-1", "J-EX-1")

        skills = self._create_match_collection([r1])
        experience = self._create_match_collection([r2])
        empty = self._create_match_collection([])

        rules = CanonicalMatchingRules(validation_mode="STRICT")
        res = self._service.build(
            skill_matches=skills,
            experience_matches=experience,
            education_matches=empty,
            project_matches=empty,
            certification_matches=empty,
            rules=rules,
        )

        self.assertEqual(2, len(res.results))
        self.assertEqual(0, res.statistics.duplicate_count)
        self.assertEqual(0, res.statistics.validation_error_count)
        self.assertEqual(0, res.validation_summary.total_errors)

    def test_strict_validation_fails_on_malformed_match(self) -> None:
        """Validator raises MatchValidationError under STRICT mode when provenance or IDs are missing."""
        # Missing provenance
        r1 = self._create_match_result("M1", "SkillMatcher", "R-SK-1", "J-SK-1", prov=False)
        skills = self._create_match_collection([r1])
        empty = self._create_match_collection([])

        rules_strict = CanonicalMatchingRules(validation_mode="STRICT")
        with self.assertRaises(MatchValidationError):
            self._service.build(
                skill_matches=skills,
                experience_matches=empty,
                education_matches=empty,
                project_matches=empty,
                certification_matches=empty,
                rules=rules_strict,
            )

        # Under LENIENT mode, it compiles but records the errors in summary
        rules_lenient = CanonicalMatchingRules(validation_mode="LENIENT")
        res = self._service.build(
            skill_matches=skills,
            experience_matches=empty,
            education_matches=empty,
            project_matches=empty,
            certification_matches=empty,
            rules=rules_lenient,
        )
        self.assertEqual(1, len(res.results))
        self.assertEqual(1, res.statistics.validation_error_count)
        self.assertEqual(1, res.validation_summary.total_errors)
        self.assertEqual("provenance", res.validation_summary.errors[0].field)

    def test_duplicate_policy_resolution(self) -> None:
        """Duplicate resolver respects KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, and KEEP_ALL policies."""
        # Duplicate pair: R-SK-1 and J-SK-1
        r1 = self._create_match_result("M1", "SkillMatcher", "R-SK-1", "J-SK-1", confidence=0.5)
        r2 = self._create_match_result("M2", "SkillMatcher", "R-SK-1", "J-SK-1", confidence=0.9)
        skills = self._create_match_collection([r1, r2])
        empty = self._create_match_collection([])

        # Policy: KEEP_FIRST
        rules = CanonicalMatchingRules(duplicate_policy="KEEP_FIRST")
        res = self._service.build(skills, empty, empty, empty, empty, rules)
        self.assertEqual(1, len(res.results))
        self.assertEqual("M1", res.results[0].match_id)
        self.assertEqual(1, res.statistics.duplicate_count)

        # Policy: KEEP_LAST
        rules = CanonicalMatchingRules(duplicate_policy="KEEP_LAST")
        res = self._service.build(skills, empty, empty, empty, empty, rules)
        self.assertEqual(1, len(res.results))
        self.assertEqual("M2", res.results[0].match_id)

        # Policy: KEEP_HIGHEST_CONFIDENCE
        rules = CanonicalMatchingRules(duplicate_policy="KEEP_HIGHEST_CONFIDENCE")
        res = self._service.build(skills, empty, empty, empty, empty, rules)
        self.assertEqual(1, len(res.results))
        self.assertEqual("M2", res.results[0].match_id)

        # Policy: KEEP_ALL
        rules = CanonicalMatchingRules(duplicate_policy="KEEP_ALL")
        res = self._service.build(skills, empty, empty, empty, empty, rules)
        self.assertEqual(2, len(res.results))
        self.assertEqual(0, res.statistics.duplicate_count)

    def test_cross_validation_duplicate_match_id(self) -> None:
        """CrossMatchValidator detects and handles duplicate match IDs across collections."""
        r1 = self._create_match_result("SAME-ID", "SkillMatcher", "R-SK-1", "J-SK-1")
        r2 = self._create_match_result("SAME-ID", "ExperienceMatcher", "R-EX-1", "J-EX-1")
        
        skills = self._create_match_collection([r1])
        experience = self._create_match_collection([r2])
        empty = self._create_match_collection([])

        rules_strict = CanonicalMatchingRules(validation_mode="STRICT")
        with self.assertRaises(CrossMatchValidationError):
            self._service.build(skills, experience, empty, empty, empty, rules_strict)

        rules_lenient = CanonicalMatchingRules(validation_mode="LENIENT")
        res = self._service.build(skills, experience, empty, empty, empty, rules_lenient)
        self.assertEqual(2, len(res.results))
        self.assertEqual(1, res.validation_summary.total_errors)
        self.assertIn("Duplicate match_id detected", res.validation_summary.errors[0].message)

    def test_deterministic_ordering(self) -> None:
        """CanonicalMatchCollection ordering is sorted by matcher_type, resume_feature_id, job_feature_id."""
        r_ex = self._create_match_result("M2", "ExperienceMatcher", "R-EX-1", "J-EX-1")
        r_sk = self._create_match_result("M1", "SkillMatcher", "R-SK-1", "J-SK-1")
        
        # In combined array, experience comes before skill, but ordering rule should sort SkillMatcher first.
        skills = self._create_match_collection([r_sk])
        experience = self._create_match_collection([r_ex])
        empty = self._create_match_collection([])

        res = self._service.build(skills, experience, empty, empty, empty)
        
        self.assertEqual("ExperienceMatcher", res.results[0].matcher_type)
        self.assertEqual("SkillMatcher", res.results[1].matcher_type)


    def test_immutability(self) -> None:
        """DTO models raise error when attempting to mutate attributes."""
        stats = MatchStatistics(
            total_resume_features=5,
            total_job_features=5,
            total_matches=1,
            duplicate_count=0,
            validation_error_count=0,
            warning_count=0,
        )
        summary = ValidationSummary(total_errors=0, total_warnings=0)
        collection = CanonicalMatchCollection(
            results=(),
            statistics=stats,
            validation_summary=summary,
        )

        with self.assertRaises(ValidationError if hasattr(collection, "__setattr__") else TypeError):
            # Attempt mutation
            collection.results = ("test",)  # type: ignore

    def test_thread_safety(self) -> None:
        """Service pipeline execution executes concurrently without race conditions or state pollution."""
        r1 = self._create_match_result("M1", "SkillMatcher", "R-SK-1", "J-SK-1")
        skills = self._create_match_collection([r1])
        empty = self._create_match_collection([])

        errors: list[Exception] = []

        def run_build() -> None:
            try:
                res = self._service.build(skills, empty, empty, empty, empty)
                self.assertEqual(1, len(res.results))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_build) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread safety failure: {errors}")
