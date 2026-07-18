"""Unit tests for Certification Matching.

Purpose:
    Verify CertificationMatcher matching logic, candidate builders, normalizers,
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
from ats_engine.domain.matching.certification.matcher import CertificationMatcher


class CertificationMatchingTests(unittest.TestCase):
    """Test suite validating CertificationMatcher candidate pipeline and constraints."""

    def setUp(self) -> None:
        """Set up registry and service context."""
        self._registry = FeatureMatcherRegistry()
        self._registry.register("certification", CertificationMatcher)
        self._service = MatchingService(self._registry)

    def _create_cert_feature(
        self,
        fid: str,
        name: str,
        source_id: str | None,
        org: str | None = None,
        category: FeatureCategory = FeatureCategory.CERTIFICATION,
    ) -> Feature:
        """Helper to create Feature mock instances."""
        return Feature(
            feature_id=fid,
            name=name,
            category=category,
            value={
                "certification_name": name,
                "issuing_organization": org,
            },
            provenance=FeatureProvenance(
                source_entity_id=source_id,
                source_entity_type=category.value,
            ),
            metadata=FeatureMetadata(
                creation_timestamp="2026-07-13T20:00:00Z",
                extractor_name="CertificationFeatureExtractor",
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
            projects=FeatureCollection(statistics=FeatureEngineeringStatistics(), context=col.context),
            certifications=col,
            statistics=FeatureStatistics(total_feature_count=len(features)),
            validation_summary=ValidationSummary(
                status="VALID",
                validation_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
            ),
        )

    def test_canonical_id_match(self) -> None:
        """CertificationMatcher matches features with identical canonical IDs."""
        f_res = self._create_cert_feature("FEAT-CERT-01", "AWS Solutions Architect", "CERT-01")
        f_job = self._create_cert_feature("FEAT-CERT-01", "AWS Solutions Architect Professional", "CERT-01")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        res = self._service.match(resume, job, ["certification"])

        self.assertEqual(1, len(res.results))
        self.assertEqual("FEAT-CERT-01", res.results[0].resume_feature_id)

    def test_structural_matching_precedence(self) -> None:
        """CertificationMatcher performs matching based on comparison modes and fields."""
        f_res = self._create_cert_feature("FEAT-CERT-RAW-1", "AWS Developer", None, org="Amazon")
        f_job = self._create_cert_feature("FEAT-CERT-RAW-2", "AWS Developer", None, org="Amazon")

        resume = self._create_canonical_collection([f_res])
        job = self._create_canonical_collection([f_job])

        rules = {
            "certification_matching_rules": {
                "comparison_mode": "ALL",
            }
        }
        res = self._service.match(resume, job, ["certification"], rules=rules)
        self.assertEqual(1, len(res.results))
