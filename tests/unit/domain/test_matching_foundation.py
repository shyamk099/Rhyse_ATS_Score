"""Unit tests for ATS Matching Engine Foundation.

Purpose:
    Verify registry, factory, immutable DTO constraints, stateless pipeline orchestration,
    deterministic sorting order, exception handling, and concurrent execution.
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
)
from ats_engine.domain.matching.exceptions import (
    ContextValidationError,
    MatcherRegistrationError,
    MatchingError,
    UnknownMatcherError,
)
from ats_engine.domain.matching.factory import FeatureMatcherFactory
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import (
    MatchCollection,
    MatchingContext,
    MatchLocation,
    MatchMetadata,
    MatchResult,
)
from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.service import MatchingService


class DummyFeatureMatcher(FeatureMatcher):
    """Test FeatureMatcher mock implementing infrastructure interface contract."""

    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Produce mock results to assert infrastructure pipeline functionality."""
        results: list[MatchResult] = []
        for r_feat in resume_features:
            for j_feat in job_features:
                results.append(
                    MatchResult(
                        match_id=f"MATCH-{r_feat.feature_id}-{j_feat.feature_id}",
                        matcher_type="DummyFeatureMatcher",
                        resume_feature_id=r_feat.feature_id,
                        job_feature_id=j_feat.feature_id,
                        metadata=MatchMetadata(
                            correlation_id=context.correlation_id,
                            matcher_type="DummyFeatureMatcher",
                            execution_timestamp="2026-07-13T20:00:00Z",
                            rules_version="matching_rules_v1.0",
                        ),
                    )
                )
        return results


class MatchingFoundationTests(unittest.TestCase):
    """Test suite validating Matching Foundation components."""

    def setUp(self) -> None:
        """Initialize empty registry and matching service."""
        self._registry = FeatureMatcherRegistry()
        self._service = MatchingService(self._registry)

    def _create_feature(self, fid: str, name: str, category: FeatureCategory) -> Feature:
        """Helper to create Feature instances."""
        return Feature(
            feature_id=fid,
            name=name,
            category=category,
            value={},
            provenance=FeatureProvenance(source_entity_id="ENT-01"),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="Mock",
                version="1.0",
            ),
        )

    def _create_canonical_collection(self, features: list[Feature]) -> CanonicalFeatureCollection:
        """Helper to create dummy canonical feature collections."""
        col = FeatureCollection(
            features=tuple(features),
            statistics=FeatureEngineeringStatistics(),
            context=FeatureExtractionContext(correlation_id="test"),
        )
        # Import models inside test to keep dependencies clean
        from ats_engine.domain.feature_engineering.models import (
            CanonicalFeatureCollection,
            FeatureStatistics,
            ValidationSummary,
        )
        return CanonicalFeatureCollection(
            skills=col,
            experience=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
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

    def test_registry_registration_and_lookup(self) -> None:
        """Registry successfully registers, retrieves, and lists matcher classes."""
        self._registry.register("dummy", DummyFeatureMatcher)

        self.assertEqual(DummyFeatureMatcher, self._registry.get("dummy"))
        self.assertIn("dummy", self._registry.list())

        # Test duplicate registration error
        with self.assertRaises(MatcherRegistrationError):
            self._registry.register("dummy", DummyFeatureMatcher)

        # Test invalid type registration error
        class NotAMatcher:
            pass

        with self.assertRaises(MatcherRegistrationError):
            self._registry.register("invalid", NotAMatcher)  # type: ignore

        # Test unknown matcher lookup error
        with self.assertRaises(UnknownMatcherError):
            self._registry.get("unknown")

    def test_factory_instantiation(self) -> None:
        """Factory cleanly instantiates FeatureMatcher instance without shared state."""
        matcher = FeatureMatcherFactory.create(DummyFeatureMatcher)
        self.assertIsInstance(matcher, DummyFeatureMatcher)

    def test_pipeline_orchestrates_matcher_and_deterministic_sorting(self) -> None:
        """Pipeline executes matcher sequentially and sorts results deterministically."""
        self._registry.register("dummy", DummyFeatureMatcher)

        f_res1 = self._create_feature("FEAT-SKILL-02", "Python", FeatureCategory.SKILL)
        f_res2 = self._create_feature("FEAT-SKILL-01", "Go", FeatureCategory.SKILL)
        f_job1 = self._create_feature("FEAT-SKILL-04", "Go Description", FeatureCategory.SKILL)
        f_job2 = self._create_feature("FEAT-SKILL-03", "Python Description", FeatureCategory.SKILL)

        resume = self._create_canonical_collection([f_res1, f_res2])
        job = self._create_canonical_collection([f_job1, f_job2])

        # Run match service
        res = self._service.match(
            resume_features=resume,
            job_features=job,
            enabled_matchers=["dummy"],
        )

        self.assertEqual(4, len(res.results))
        self.assertEqual(1, res.statistics.processed_matchers)
        self.assertEqual(4, res.statistics.match_result_count)

        # Confirm Deterministic Ordering (sorted by matcher_type, resume_feature_id, job_feature_id)
        # resume_feature_ids: FEAT-SKILL-01, FEAT-SKILL-02
        # job_feature_ids: FEAT-SKILL-03, FEAT-SKILL-04
        results = res.results
        self.assertEqual("FEAT-SKILL-01", results[0].resume_feature_id)
        self.assertEqual("FEAT-SKILL-03", results[0].job_feature_id)

        self.assertEqual("FEAT-SKILL-01", results[1].resume_feature_id)
        self.assertEqual("FEAT-SKILL-04", results[1].job_feature_id)

        self.assertEqual("FEAT-SKILL-02", results[2].resume_feature_id)
        self.assertEqual("FEAT-SKILL-03", results[2].job_feature_id)

        self.assertEqual("FEAT-SKILL-02", results[3].resume_feature_id)
        self.assertEqual("FEAT-SKILL-04", results[3].job_feature_id)

    def test_immutable_dto_constraints(self) -> None:
        """DTO models raise ValidationError when trying to mutate frozen structures."""
        from pydantic import ValidationError
        location = MatchLocation(resume_page=1, job_page=2)
        with self.assertRaises(ValidationError):
            location.resume_page = 3  # type: ignore

    def test_empty_collections_resilient(self) -> None:
        """Service executes cleanly and returns zero stats when collections are empty."""
        resume = self._create_canonical_collection([])
        job = self._create_canonical_collection([])

        res = self._service.match(
            resume_features=resume,
            job_features=job,
            enabled_matchers=[],
        )

        self.assertEqual(0, len(res.results))
        self.assertEqual(0, res.statistics.match_result_count)

    def test_invalid_parameters_raises_context_validation_error(self) -> None:
        """Service raises ContextValidationError if inputs are None."""
        resume = self._create_canonical_collection([])
        with self.assertRaises(ContextValidationError):
            self._service.match(None, resume, [])  # type: ignore

    def test_thread_safety_under_concurrent_matches(self) -> None:
        """Service performs comparisons concurrently without thread interference."""
        self._registry.register("dummy", DummyFeatureMatcher)

        f_res = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        f_job = self._create_feature("FEAT-SKILL-01", "Python", FeatureCategory.SKILL)
        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        errors: list[Exception] = []

        def run_matching() -> None:
            try:
                res = self._service.match(resume, job, ["dummy"])
                self.assertEqual(1, len(res.results))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_matching) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Concurrent matching compilation failed: {errors}")
